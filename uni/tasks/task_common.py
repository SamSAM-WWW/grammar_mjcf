import torch
import pytorch3d.transforms as transforms
from dataclasses import dataclass

@dataclass
class TaskCommon():
    alive_reward: float = 0.5
    termination_height: float = 0.4
    termination_cost: float = 2.0
    up_weight: float = 0.1
    heading_weight: float = 0.1
    actions_cost_scale: float = 0.005
    energy_cost_scale: float = 0.01
    joints_at_limit_cost_scale: float = 0.1

    def compute_reward_common(self,
            root_position: torch.tensor,    # nenv, 3
            root_orientation: torch.tensor, # nenv, 4
            actions: torch.tensor,          # nenv, max_bodies, max_dofs
            dof_pos: torch.tensor,          # nenv, max_bodies, max_dofs
            dof_vel: torch.tensor,          # nenv, max_bodies, max_dofs
            wheel_mask: torch.tensor,       # nenv, max_bodies, 1
            up_vec: torch.tensor,           # nenv, 3
            heading_vec: torch.tensor,      # nenv, 3
            target_vecs: torch.tensor,      # nenv, 3
            root_vel: torch.tensor,         # nenv, 3
            root_rel_height,
        ):
        n = root_position.shape[0]

        # reward for keeping the robot upright
        up_vec_in_base_frame = transforms.quaternion_apply(root_orientation, up_vec)
        up_reward = self.up_weight * up_vec_in_base_frame[..., 2]
        up_reward = torch.clamp(up_reward, min=0.)

        # reward for keeping the robot pointed at its target
        heading_vec_in_base_frame = transforms.quaternion_apply(root_orientation, heading_vec)
        heading_reward = self.heading_weight * (heading_vec_in_base_frame * target_vecs).sum(-1)
        heading_reward = torch.clamp(heading_reward, min=0.)

        vel_reward = 1.0 * root_vel[:,0]

        # energy penalty for movement
        actions_cost = (actions ** 2).sum(dim=(1, 2))

        dof_vel_ = dof_vel * torch.logical_not(wheel_mask.squeeze(-1))
        electricity_cost = (torch.abs(actions * dof_vel_)).sum(dim=(1,2))

        # wheel_vel = dof_vel * wheel_mask.squeeze(-1)
        # wheel_reward = 0.8 * torch.mean(torch.abs(wheel_vel), dim=(1,2))

        dof_pos_ = dof_pos * torch.logical_not(wheel_mask.squeeze(-1))
        # print(dof_pos_)
        dof_at_limit_cost = torch.sum(torch.abs(dof_pos_) > 1.3, dim=(1,2)).float()

        total_reward = (self.alive_reward + up_reward + heading_reward + vel_reward
                - self.actions_cost_scale * actions_cost
                - self.energy_cost_scale * electricity_cost
                - self.joints_at_limit_cost_scale * dof_at_limit_cost)

        # adjust reward for fallen agents
        total_reward = torch.where(root_rel_height < self.termination_height,
                                   -1 * torch.ones_like(total_reward) * self.termination_cost,
                                   total_reward)
        return total_reward


    def compute_termination_common(self, root_rel_position):
        # print(root_rel_position)
        height_termination = torch.le(root_rel_position, self.termination_height)
        # print(height_termination.shape)
        return height_termination
