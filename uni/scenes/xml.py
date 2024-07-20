from typing import Optional, List
from isaacgym import gymapi
from uni.sim import CameraSensor
from .isaac_scene import IsaacScene
from uni.utils import torch_jit_utils as tjit
import torch
import os
import numpy as np
import glob
import xml.etree.ElementTree as ET
from uni.xml_parser import XMLModel, URDFModel
from .terrain import CuriculumTerrain


def to_torch(array, dtype=torch.float, device='cuda:0', requires_grad=False):
    return torch.tensor(array, dtype=dtype, device=device, requires_grad=requires_grad)

def get_init_z(paths):
    z = []
    for path in paths:
        tree = ET.parse(path)
        z.append(float(tree.getroot().find('worldbody').find('body').get('pos').split()[2]))
    return z

class MixedXMLScene(IsaacScene):

    def __init__(self, *args, **kwargs):
        IsaacScene.__init__(self, *args, **kwargs)
        self.asset_root = None
        self.load_urdf = False

    def set_asset_root(self, path):
        self.asset_root = path

    def set_viewer_pos(self, pos: list, target: list):
        IsaacScene.set_viewer_pos(self, pos, target)

    def create_viewer(self, props: gymapi.CameraProperties = None):
        if self._viewer_pos is None:
            self.set_viewer_pos([-10., 8., 5.0], [10., 8., 3.0])
        if props is None:
            props = gymapi.CameraProperties()
            # props.height = 432 * 2
            # props.width = 768 * 2
        IsaacScene.create_viewer(self, props)

    def act(self, action: torch.Tensor):
        # print(self.joint_gears.shape, action.shape)
        self.tensor_api.dof_force_control.force = action * self.joint_gears
        self.tensor_api.dof_force_control.push()

    def create_scene(self):
        if self.asset_root is None:
            raise ValueError('You must set an asset root before calling create_scene')
        if self.load_urdf:
            self.asset_files = sorted([os.path.basename(f) for f in
                                    glob.glob(os.path.join(self.asset_root, '*.urdf'))])

            xml_models = []
            for i, asset in enumerate(self.asset_files):
                xml = URDFModel.from_path(os.path.join(self.asset_root, asset))
                print(xml.root.get_lowest_point())
                xml_models.append(xml)
            self.xml_models = [xml_models[i % len(xml_models)] for i in range(self.num_envs)]
        else:
            self.asset_files = sorted([os.path.basename(f) for f in
                                    glob.glob(os.path.join(self.asset_root, '*.xml'))])

            xml_models = []
            for i, asset in enumerate(self.asset_files):
                xml = XMLModel.from_path(os.path.join(self.asset_root, asset))
                # print(xml.root.get_lowest_point())
                xml_models.append(xml)
            self.xml_models = [xml_models[i % len(xml_models)] for i in range(self.num_envs)]

        self.sim = self.gym.create_sim(self.device_id, self.device_id, gymapi.SIM_PHYSX,
                                       self.sim_params)

        # self.terrain.create(self.gym, self.sim)
        terrain_type = 'curiculum' if not self.test else 'test'
        self.terrain_indexer = CuriculumTerrain(self.num_envs, terrain_type, self.gym, self.sim, self.device)

        lower = gymapi.Vec3(0., 0., 0.)
        upper = gymapi.Vec3(0., 0., 0.)

        asset_options = gymapi.AssetOptions()
        asset_options.default_dof_drive_mode = gymapi.DOF_MODE_EFFORT
        asset_options.angular_damping = 0.0
        asset_options.use_mesh_materials = True

        start_pose = gymapi.Transform()
        self.start_rotation = torch.tensor([start_pose.r.x, start_pose.r.y, start_pose.r.z,
                                            start_pose.r.w],
                                           device=self.device)
        self.inv_start_rot = tjit.quat_conjugate(self.start_rotation).repeat((self.num_envs, 1))
        self.num_dof = []
        self.num_bodies = []
        self.envs = []
        self.joint_gears = []
        self.cameras = []
        self.dof_limits_lower = []
        self.dof_limits_upper = []
        if self.load_urdf:
            self.init_z = [-xml.root.get_lowest_point() for xml in xml_models]
        else:
            self.init_z = [xml.get_height()-xml.root.get_lowest_point() for xml in xml_models]
        if self.load_urdf:
            asset_options.replace_cylinder_with_capsule = True
            asset_options.override_com = True
            asset_options.override_inertia = True
            asset_options.flip_visual_attachments = True
            asset_options.collapse_fixed_joints = False
            self.urdf_assets = [self.gym.load_asset(self.sim, self.asset_root, path, asset_options)
                                for path in self.asset_files]
        else:
            self.xml_assets = [self.gym.load_asset(self.sim, self.asset_root, path, asset_options)
                           for path in self.asset_files]
            self.urdf_assets = self.xml_assets

        # add body force sensors
        if self.load_urdf:
            for asset in self.urdf_assets:
                num_bodies = self.gym.get_asset_rigid_body_count(asset)
                sensor_pose = gymapi.Transform()
                sensor_props = gymapi.ForceSensorProperties()
                sensor_props.enable_forward_dynamics_forces = True
                sensor_props.enable_constraint_solver_forces = True
                sensor_props.use_world_frame = True
                for body_idx in range(num_bodies):
                    ind = self.gym.create_asset_force_sensor(asset, body_idx, sensor_pose,
                                                             sensor_props)
        else:
            for asset in self.xml_assets:
                num_bodies = self.gym.get_asset_rigid_body_count(asset)
                sensor_pose = gymapi.Transform()
                sensor_props = gymapi.ForceSensorProperties()
                sensor_props.enable_forward_dynamics_forces = True
                sensor_props.enable_constraint_solver_forces = True
                sensor_props.use_world_frame = True
                for body_idx in range(num_bodies):
                    ind = self.gym.create_asset_force_sensor(asset, body_idx, sensor_pose,
                                                         sensor_props)
        if not self.test:
            self._get_env_origins()
        for i in range(self.num_envs):
            asset = self.urdf_assets[i % len(self.urdf_assets)] if self.load_urdf else self.xml_assets[i % len(self.xml_assets)]
            start_pose = gymapi.Transform()
            start_pose.p.z = self.init_z[i % len(self.init_z)]
            if self.test:
                pos = [-1., 8., 0.]
            else:
                pos = self.env_origins[i].clone()
            start_pose.p += gymapi.Vec3(*pos)

            env_ptr = self.gym.create_env(
                self.sim, lower, upper, self.num_per_row
            )
            handle = self.gym.create_actor(env_ptr, asset, start_pose, "actor", i, 1, 0)
            if self.load_urdf:
                props = self.gym.get_asset_dof_properties(asset)
                self.gym.set_actor_dof_properties(env_ptr, handle, props)
                urdf_model = self.xml_models[i]
                motor_efforts = [80]*12
                self.joint_gears.append(to_torch(motor_efforts, device=self.device))
            else:
                actuator_props = self.gym.get_asset_actuator_properties(asset)
                motor_efforts = [prop.motor_effort for prop in actuator_props]
                self.joint_gears.append(to_torch(motor_efforts, device=self.device))
                props = self.gym.get_actor_dof_properties(env_ptr, handle)
                for prop_ind, prop in enumerate(props):
                    if prop[0]:
                        prop[4] = 2 * np.pi
                        prop[5] = motor_efforts[prop_ind]
                    else:
                        prop[4] = 6 * np.pi
                        prop[5] = motor_efforts[prop_ind]
                self.gym.set_actor_dof_properties(env_ptr, handle, props)

            num_dof = self.gym.get_asset_dof_count(asset)
            num_bodies = self.gym.get_asset_rigid_body_count(asset)
            self.num_dof.append(num_dof)
            self.num_bodies.append(num_bodies)

            # print(self.joint_gears)

            self.gym.enable_actor_dof_force_sensors(env_ptr, handle)
            if self.create_eval_sensors:
                props = gymapi.CameraProperties()
                props.height = 1024
                props.width = 1024
                self.cameras.append(CameraSensor(self.gym, self.sim, env_ptr, props))
                t = gymapi.Transform()
                t.p = gymapi.Vec3(0, -3, 1)
                t.r = gymapi.Quat.from_axis_angle(gymapi.Vec3(0, 0, 1), np.radians(90))
                body_handle = self.gym.get_actor_rigid_body_handle(env_ptr, handle, 0)
                self.cameras[-1].attach_camera_to_body(body_handle, t, gymapi.FOLLOW_POSITION)

            self.envs.append(env_ptr)
            dof_prop = self.gym.get_actor_dof_properties(env_ptr, handle)
            dof_limits_lower = []
            dof_limits_upper = []
            for j in range(num_dof):
                if dof_prop['lower'][j] > dof_prop['upper'][j]:
                    dof_limits_lower.append(dof_prop['upper'][j])
                    dof_limits_upper.append(dof_prop['lower'][j])
                else:
                    dof_limits_lower.append(dof_prop['lower'][j])
                    dof_limits_upper.append(dof_prop['upper'][j])

            self.dof_limits_lower.append(to_torch(dof_limits_lower, device=self.device))
            self.dof_limits_upper.append(to_torch(dof_limits_upper, device=self.device))
        self.joint_gears = torch.cat(self.joint_gears, dim=0)
        self.dof_limits_lower = torch.cat(self.dof_limits_lower, dim=0)
        self.dof_limits_upper = torch.cat(self.dof_limits_upper, dim=0)
        if self.homogeneous_envs:
            self.joint_gears = self.joint_gears.view(self.num_envs, -1)
            self.dof_limits_lower = self.dof_limits_lower.view(self.num_envs, -1)
            self.dof_limits_upper = self.dof_limits_upper.view(self.num_envs, -1)

        self.gym.prepare_sim(self.sim)

        self.initial_dof_pos = torch.zeros_like(self.tensor_api.dof_state.position, device=self.device)
        zero_tensor = torch.tensor([0.0], device=self.device)
        self.initial_dof_pos = torch.where(self.dof_limits_lower > zero_tensor, self.dof_limits_lower,
                                           torch.where(self.dof_limits_upper < zero_tensor,
                                                       self.dof_limits_upper, self.initial_dof_pos))
        self.initial_dof_vel = torch.zeros_like(self.tensor_api.dof_state.velocity)
        self.initial_root_state = self.tensor_api.actor_root_state.state.clone()
        self.initial_root_state[..., 7:13] = 0  # set lin_vel and ang_vel to 0

        self.env_dof_inds = [0] + np.cumsum(self.num_dof).tolist()


        self.actor_inds = torch.tensor(
                [self.gym.get_actor_index(env, 0, gymapi.IndexDomain.DOMAIN_SIM)
                 for env in self.envs],
                dtype=torch.long, device=self.device)

        self.terrain_indexer.set_actor_inds(self.actor_inds)


    def _get_env_origins(self):
        """ Sets environment origins. On rough terrain the origins are defined by the terrain platforms.
            Otherwise create a grid.
        """
        self.custom_origins = True
        self.env_origins = torch.zeros(self.num_envs, 3, device=self.device, requires_grad=False)
        # put robots at the origins defined by the terrain
        max_init_level = self.terrain_indexer.max_init_terrain_level
        self.terrain_levels = torch.randint(0, max_init_level+1, (self.num_envs,), device=self.device)
        self.terrain_types = torch.div(torch.arange(self.num_envs, device=self.device), (self.num_envs/self.terrain_indexer.num_cols), rounding_mode='floor').to(torch.long)
        self.max_terrain_level = self.terrain_indexer.num_rows
        self.terrain_origins = torch.from_numpy(self.terrain_indexer.env_origins).to(self.device).to(torch.float)
        self.env_origins[:] = self.terrain_origins[self.terrain_levels, self.terrain_types]
    
    def _update_terrain_curriculum(self, env_ids):
        """ Implements the game-inspired curriculum.

        Args:
            env_ids (List[int]): ids of environments being reset
        """
        actor_ids = self.actor_inds[env_ids]
        root_states = self.tensor_api.actor_root_state.state[actor_ids] 
        distance = torch.norm(root_states[:, :2] - self.env_origins[env_ids, :2], dim=1)
        # robots that walked far enough progress to harder terains
        move_up = distance > self.terrain_indexer.env_length / 2
        # robots that walked less than half of their required distance go to simpler terrains
        # print(distance)
        move_down = (distance < 0.05) * ~move_up
        self.terrain_levels[env_ids] += 1 * move_up - 1 * move_down
        # Robots that solve the last level are sent to a random one
        self.terrain_levels[env_ids] = torch.where(self.terrain_levels[env_ids]>=self.max_terrain_level,
                                                   torch.randint_like(self.terrain_levels[env_ids], self.max_terrain_level),
                                                   torch.clip(self.terrain_levels[env_ids], 0)) # (the minumum level is zero)
        self.env_origins[env_ids] = self.terrain_origins[self.terrain_levels[env_ids], self.terrain_types[env_ids]]
    

    def reset(self, env_ids: Optional[torch.Tensor] = None):
        if self.test:
            return
        if env_ids is None:
            env_ids = tuple(range(self.num_envs))
            env_ids = torch.tensor(env_ids, dtype=torch.long, device=self.device)
        elif env_ids.dtype is not torch.long:
            env_ids = env_ids.long()
            self._update_terrain_curriculum(env_ids)
        else:
            self._update_terrain_curriculum(env_ids)

        noise = torch.rand_like(self.initial_dof_pos) * 0.4 - 0.2
        init_pos = self.initial_dof_pos + noise
        torch.minimum(init_pos, self.dof_limits_upper, out=init_pos)
        torch.maximum(init_pos, self.dof_limits_lower, out=init_pos)
        init_vel = torch.rand_like(self.initial_dof_vel) * 0.2 - 0.1
        if self.homogeneous_envs:
            self.tensor_api.dof_state.position[env_ids] = init_pos[env_ids]
            self.tensor_api.dof_state.velocity[env_ids] = init_vel[env_ids]
        else:
            for env_id in env_ids:
                start, end = self.env_dof_inds[env_id], self.env_dof_inds[env_id + 1]
                self.tensor_api.dof_state.position[start:end] = init_pos[start:end]
                self.tensor_api.dof_state.velocity[start:end] = init_vel[start:end]
                z = self.init_z[env_id % len(self.init_z)]
                actor_id = self.actor_inds[env_id]
                initial_root_state = self.initial_root_state[actor_id].clone()
                initial_root_state[:3] = self.env_origins[env_id].clone()
                initial_root_state[:3] = self.env_origins[env_id].clone() + torch.tensor([0,0,z], requires_grad=False).to(initial_root_state.device)
                self.tensor_api.actor_root_state.state[actor_id] = initial_root_state

        env_ids_int32 = env_ids.int()
        self.tensor_api.dof_state.push(env_ids_int32)
        self.tensor_api.actor_root_state.push(env_ids_int32)

    def step(self, *args, **kwargs):
        IsaacScene.step(self, *args, **kwargs)

