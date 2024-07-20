"""Some simple networks."""
from uni.rl.modules import Policy, ActorCriticBase, PolicyBase, ValueFunctionBase
from uni.rl.modules import DiagGaussian, Normal
from uni.rl.networks.base import FeedForwardNet
import torch
import torch.nn as nn
import gin
import mup
import numpy as np
from .transformer_base import TransformerEncoderLayer, TransformerEncoder
from .positional_encodings import TreePositionalEncoding


class MaskedNormal(Normal):
    def __init__(self, *args, mask=None, **kwargs):
        Normal.__init__(self, *args, **kwargs)
        self.mask = mask

    def log_prob(self, ac):
        logp = Normal.log_prob(self, ac)
        if self.mask is not None:
            logp = logp * self.mask
        return logp.view(logp.shape[0], -1).sum(-1)

    def entropy(self):
        ent = Normal.entropy(self)
        if self.mask is not None:
            ent = ent * self.mask
        return ent.view(ent.shape[0], -1).sum(-1)

    def kl(self, other):
        batch_size = other.stddev.shape[0]
        dim = self.mask.view(batch_size, -1).sum(1)

        t1 = torch.log(other.stddev / self.stddev)
        t2 = (self.variance + (self.mean - other.mean).pow(2)) / (2.0 * other.variance)

        t1 = (t1 * self.mask).view(batch_size, -1).sum(1)
        t2 = (t2 * self.mask).view(batch_size, -1).sum(1)

        return t1 + t2 - 0.5 * dim


class MaskedDiagGaussian(DiagGaussian):
    def forward(self, x, mask, return_logstd=False):
        mean = self.fc_mean(x)
        if self.constant_log_std:
            logstd = torch.clamp(self.logstd, self.log_std_min, self.log_std_max)
        else:
            logstd = torch.clamp(self.fc_logstd(x), self.log_std_min, self.log_std_max)
        if return_logstd:
            return MaskedNormal(mean, logstd.exp(), mask=mask), logstd
        else:
            return MaskedNormal(mean, logstd.exp(), mask=mask)


class ProprioceptiveObservationEmbedding(nn.Module):
    def __init__(
        self,
        observation_space,
        dmodel,
        pos_encoding,
        activation_fn=nn.ReLU,
        separate_global_embedding=False,
    ):
        nn.Module.__init__(self)
        self.observation_space = observation_space
        assert dmodel % 4 == 0
        self.demb = int(dmodel / 4)
        self.dmodel = dmodel
        self.dgeom = observation_space["geom"]["obs"].shape[-1]
        self.djoint = observation_space["joint"]["obs"].shape[-1]
        self.dwheel = observation_space["joint"]["obs"].shape[-1] - 3
        self.dinertia = observation_space["inertia"]["obs"].shape[-1]
        self.droot = observation_space["root"]["obs"].shape[-1]
        self.dtask = observation_space["task"]["obs"].shape[-1]
        self.dglobal = self.droot + self.dtask
        self.activation_fn = activation_fn
        self.separate_global_embedding = separate_global_embedding

        print(
            f"geom: {observation_space['geom']['obs'].shape}, joint: {observation_space['joint']['obs'].shape}, wheel: {self.dwheel}, inertia: {observation_space['inertia']['obs'].shape}, "
            f"root: {self.droot}, task: {self.dtask}, global: {self.dglobal}"
        )

        # Geom embeddings
        self.geom_emb = FeedForwardNet(
            self.dgeom,
            units=[2 * self.demb, self.demb],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.geom_norm = nn.LayerNorm(self.demb)

        # Joint embeddings
        print(self.djoint, [2 * self.demb, self.demb - 8], self.dmodel)
        self.joint_emb = FeedForwardNet(
            self.djoint,
            units=[2 * self.demb, int(self.demb/8*7)],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.joint_norm = nn.LayerNorm(self.demb)
        self.individual_joint_norm = nn.LayerNorm(self.demb)

        # Wheel embeddings
        self.wheel_emb = FeedForwardNet(
            self.dwheel,
            units=[2 * self.demb, int(self.demb/8*7)],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.wheel_norm = nn.LayerNorm(self.demb)
        self.individual_wheel_norm = nn.LayerNorm(self.demb)

        self.type_emb = nn.Embedding(2, int(self.demb/8))

        # Inertia embeddings
        self.inertia_emb = FeedForwardNet(
            self.dinertia,
            units=[2 * self.demb, self.demb],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.inertia_norm = nn.LayerNorm(self.demb)

        # Force Sensor embeddings
        self.inertia_emb = FeedForwardNet(
            self.dinertia,
            units=[2 * self.demb, self.demb],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.inertia_norm = nn.LayerNorm(self.demb)

        # Global embeddings
        self.global_emb = FeedForwardNet(
            self.dglobal,
            units=[2 * self.demb, self.demb],
            activation_fn=self.activation_fn,
            activate_last=False,
        )
        self.global_norm = nn.LayerNorm(self.demb)

        if self.separate_global_embedding:
            self.global_emb2 = FeedForwardNet(
                self.dglobal,
                units=[2 * self.dmodel, self.dmodel],
                activation_fn=self.activation_fn,
                activate_last=False,
            )
            self.global_norm2 = nn.LayerNorm(self.dmodel)

        # Positional Encoding
        if pos_encoding is not None:
            self.pos_encoding = pos_encoding(self.dmodel, 100)
        else:
            self.pos_encoding = None

    def forward(self, obs):
        # compute embeddings
        geom_emb = self.geom_norm(
            torch.sum(self.geom_emb(obs["geom"]["obs"]) * obs["geom"]["mask"], dim=2)
        )

        type_obs = self.type_emb(obs["joint"]["type"]).squeeze(-2)

        # joint_obs = torch.cat([type_obs, obs["joint"]["obs"]], dim=-1)
        joint_emb = self.joint_emb(obs["joint"]["obs"])
        joint_emb = torch.cat([type_obs, joint_emb], dim=-1)
        individual_joint_emb = self.individual_joint_norm(joint_emb)
        joint_emb = self.joint_norm(torch.sum(joint_emb * obs["joint"]["mask"], dim=-2))

        # wheel_obs = torch.cat([type_obs, obs["joint"]["obs"][..., 1:self.djoint-2]], dim=-1)
        wheel_emb = self.wheel_emb(obs["joint"]["obs"][..., 1:self.djoint-2])
        wheel_emb = torch.cat([type_obs, wheel_emb], dim=-1)
        individual_wheel_emb = self.individual_wheel_norm(wheel_emb)
        wheel_emb = self.wheel_norm(torch.sum(wheel_emb * obs["joint"]["wheel_mask"], dim=-2))

        joint_emb[obs["joint"]["wheel_mask"][:,:,0].squeeze(-1)] = wheel_emb[obs["joint"]["wheel_mask"][:,:,0].squeeze(-1)]
        max_joints = individual_joint_emb.shape[2]
        individual_joint_emb[obs["joint"]["wheel_mask"][:,:,0].repeat(1,1,max_joints)] = individual_wheel_emb[obs["joint"]["wheel_mask"][:,:,0].repeat(1,1,max_joints)]
        
        inertia_emb = self.inertia_norm(self.inertia_emb(obs["inertia"]["obs"]))

        global_obs = torch.cat([obs["root"]["obs"], obs["task"]["obs"]], dim=-1)
        global_emb = self.global_norm(
            self.global_emb(global_obs).view(-1, 1, self.demb)
        )
        global_emb = global_emb.expand(-1, inertia_emb.shape[1], -1)

        emb = torch.cat([geom_emb, joint_emb, inertia_emb, global_emb], dim=-1)
        if self.pos_encoding is not None:
            if isinstance(self.pos_encoding, TreePositionalEncoding):
                emb = self.pos_encoding(emb, obs["joint"]["parents"])
            else:
                emb = self.pos_encoding(emb)

        if self.separate_global_embedding:
            global_emb2 = self.global_norm2(
                self.global_emb2(global_obs).view(-1, 1, self.dmodel)
            )
        else:
            global_emb2 = None

        return emb, individual_joint_emb, global_emb2

    def mup_init(self):
        for module in [
            self.geom_emb,
            self.joint_emb,
            self.wheel_emb,
            self.type_emb,
            self.inertia_emb,
            self.global_emb,
        ]:
            for name, param in module.named_parameters():
                if "bias" in name:
                    nn.init.constant_(param, 0.0)
                else:
                    mup.init.kaiming_uniform_(param, np.sqrt(5.0))


class TerrainEmbedding(nn.Module):
    def __init__(
        self, observation_space, dmodel, nlayers=3, activation_fn=nn.ReLU, num_heads=1
    ):
        nn.Module.__init__(self)
        self.num_heads = num_heads
        self.observation_space = observation_space
        self.net = FeedForwardNet(
            observation_space["terrain"]["obs"].shape[0],
            units=[dmodel//2, dmodel//2, num_heads * (dmodel//2)],
            activation_fn=activation_fn,
            activate_last=False,
        )
        self.upper_net = FeedForwardNet(
            observation_space["upper_terrain"]["obs"].shape[0],
            units=[dmodel//2, dmodel//2, num_heads * (dmodel//2)],
            activation_fn=activation_fn,
            activate_last=False,
        )

    def forward(self, obs):
        terrain_emb = self.net(obs["terrain"]["obs"])
        upper_terrain_emb = self.upper_net(obs["upper_terrain"]["obs"])
        return terrain_emb.chunk(self.num_heads, dim=1), upper_terrain_emb.chunk(self.num_heads, dim=1)

    def mup_init(self):
        for name, param in self.net.named_parameters():
            if "bias" in name:
                nn.init.constant_(param, 0.0)
            else:
                mup.init.kaiming_uniform_(param, np.sqrt(5.0))
        for name, param in self.upper_net.named_parameters():
            if "bias" in name:
                nn.init.constant_(param, 0.0)
            else:
                mup.init.kaiming_uniform_(param, np.sqrt(5.0))

def get_sinusoid_encoding_table(n_position, d_hid): 
    ''' Sinusoid position encoding table ''' 
    # TODO: make it with torch instead of numpy 
    def get_position_angle_vec(position): 
        return [position / np.power(10000, 2 * (hid_j // 2) / d_hid) for hid_j in range(d_hid)] 

    sinusoid_table = np.array([get_position_angle_vec(pos_i) for pos_i in range(n_position)]) 
    sinusoid_table[:, 0::2] = np.sin(sinusoid_table[:, 0::2]) # dim 2i 
    sinusoid_table[:, 1::2] = np.cos(sinusoid_table[:, 1::2]) # dim 2i+1 

    return  torch.tensor(sinusoid_table,dtype=torch.float, requires_grad=False).unsqueeze(0) 

class BasicControlTransformer(ActorCriticBase):
    def __init__(
        self,
        observation_space,
        action_space,
        nlayers=3,
        dmodel=256,
        nheads=4,
        activation_fn=nn.ReLU,
        pos_encoding=None,
        include_terrain=False,
        num_terrain_heads=1,
        use_mup=True,
    ):
        self.activation_fn = activation_fn
        self.nlayers = nlayers
        self.dmodel = dmodel
        self.nheads = nheads
        self.pos_encoding = pos_encoding
        self.separate_global_embedding = False
        self.include_terrain = include_terrain
        self.num_terrain_heads = num_terrain_heads
        self.use_mup = use_mup
        ActorCriticBase.__init__(self, observation_space, action_space)

    def build(self):
        self.obs_emb = ProprioceptiveObservationEmbedding(
            self.observation_space,
            self.dmodel,
            pos_encoding=self.pos_encoding,
            activation_fn=self.activation_fn,
            separate_global_embedding=self.separate_global_embedding,
        )
        self.demb = self.obs_emb.demb

        dout = self.dmodel
        if self.include_terrain:
            self.terrain_emb = TerrainEmbedding(
                self.observation_space,
                self.dmodel,
                nlayers=3,
                activation_fn=self.activation_fn,
                num_heads=self.num_terrain_heads,
            )
            dout += self.dmodel

        encoder_layer = TransformerEncoderLayer(
            self.dmodel,
            self.nheads,
            dim_feedforward=2 * self.dmodel,
            activation_fn=self.activation_fn,
            batch_first=True,
            norm_first=True,
        )
        self.encoder = TransformerEncoder(encoder_layer, num_layers=self.nlayers)

        self.register_buffer('pos_embed', get_sinusoid_encoding_table(50, self.dmodel))

        if self.use_mup:
            self.value_decoder = nn.Sequential(
                nn.Linear(dout, self.dmodel),
                self.activation_fn(),
                mup.MuReadout(self.dmodel, 1),
            )
        else:
            self.value_decoder = nn.Sequential(
                nn.Linear(dout, self.dmodel),
                self.activation_fn(),
                nn.Linear(self.dmodel, 1),
            )

        self.action_decoder = FeedForwardNet(
            dout + self.demb,
            units=[self.dmodel],
            activation_fn=self.activation_fn,
            activate_last=True,
        )
        self.action_dist = MaskedDiagGaussian(self.dmodel, 1, use_mup=self.use_mup)

    def forward(self, obs):
        emb, individual_joint_emb, _ = self.obs_emb(obs)

        # run transformer layers
        padding_mask = obs["inertia"]["mask"].squeeze(-1)

        x = self.encoder(emb, key_padding_mask=torch.logical_not(padding_mask))
        if self.include_terrain:
            terrain_emb, upper_terrain_emb = self.terrain_emb(obs)
            terrain_emb, upper_terrain_emb = terrain_emb[0], upper_terrain_emb[0]
            terrain_emb = terrain_emb.unsqueeze(1).expand(-1, x.shape[1], -1)
            upper_terrain_emb = upper_terrain_emb.unsqueeze(1).expand(-1, x.shape[1], -1)
            x = torch.cat([x, terrain_emb, upper_terrain_emb], dim=2)

        # decode actions
        n_joints = individual_joint_emb.shape[2]
        x_joint = x.unsqueeze(2).expand(-1, -1, n_joints, -1)
        action_emb = torch.cat([x_joint, individual_joint_emb], dim=3)
        action_emb = self.action_decoder(action_emb)
        dist = self.action_dist(action_emb, torch.logical_or(obs["joint"]["mask"], obs["joint"]["wheel_mask"]).squeeze(-1))
        
        # decode value
        value_out = self.value_decoder(x) * padding_mask.unsqueeze(-1)
        value = value_out.sum(1) / padding_mask.sum(1, keepdims=True)
        return dist, value

    def mup_init(self):
        self.obs_emb.mup_init()
        self.encoder.mup_init()
        self.action_dist.mup_init()
        if self.include_terrain:
            self.terrain_emb.mup_init()

        for module in [self.value_decoder, self.action_decoder]:
            for name, param in module.named_parameters():
                if "bias" in name:
                    nn.init.constant_(param, 0.0)
                else:
                    mup.init.kaiming_uniform_(param, np.sqrt(5.0))


@gin.configurable(module="rl")
def basic_transformer_policy(
    env,
    nlayers=3,
    dmodel=256,
    nheads=4,
    activation_fn=nn.ReLU,
    pos_encoding=None,
    include_terrain=False,
    num_terrain_heads=1,
    use_mup=True,
):
    if use_mup:
        model = BasicControlTransformer(
            env.observation_space,
            env.action_space,
            nlayers=nlayers,
            dmodel=dmodel,
            nheads=nheads,
            activation_fn=activation_fn,
            pos_encoding=pos_encoding,
            include_terrain=include_terrain,
            num_terrain_heads=num_terrain_heads,
            use_mup=use_mup,
        )

        base = BasicControlTransformer(
            env.observation_space,
            env.action_space,
            nlayers=nlayers,
            dmodel=256,
            nheads=4,
            activation_fn=activation_fn,
            pos_encoding=pos_encoding,
            include_terrain=include_terrain,
            num_terrain_heads=num_terrain_heads,
            use_mup=use_mup,
        )

        delta = BasicControlTransformer(
            env.observation_space,
            env.action_space,
            nlayers=nlayers,
            dmodel=32,
            nheads=1,
            activation_fn=activation_fn,
            pos_encoding=pos_encoding,
            include_terrain=include_terrain,
            num_terrain_heads=num_terrain_heads,
            use_mup=use_mup,
        )

        mup.set_base_shapes(model, base, delta=delta)
        model.mup_init()
        del base
        del delta
        return Policy(model)

    else:
        base = BasicControlTransformer(
            env.observation_space,
            env.action_space,
            nlayers=nlayers,
            dmodel=dmodel,
            nheads=nheads,
            activation_fn=activation_fn,
            pos_encoding=pos_encoding,
            include_terrain=include_terrain,
            num_terrain_heads=num_terrain_heads,
            use_mup=use_mup,
        )
        return Policy(base)
