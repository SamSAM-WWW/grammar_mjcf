import dataclasses
from typing import Sequence
import random
from isaacgym import gymapi
import isaacgym.terrain_utils as tu
import numpy as np
import gin
import torch
from gym.spaces import Box
from pytorch3d import transforms

class CuriculumTerrain():
    static_friction = 1.0
    dynamic_friction = 1.0
    restitution = 0.
    measured_points_x = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] # 1mx1.6m rectangle (without center line)
    measured_points_y = [-0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5]
    max_init_terrain_level = 5 # starting curriculum state
    terrain_length = 8.
    terrain_width = 8.
    num_rows= 10 # number of terrain rows (levels)
    num_cols = 20 # number of terrain cols (types)
    # terrain types: [smooth slope, rough slope, stairs up, stairs down, discrete]
    terrain_proportions = [0.1, 0.1, 0.35, 0.25, 0.2]
    # trimesh only:
    slope_treshold = 0.75 # slopes above this threshold will be corrected to vertical surfaces
    horizontal_scale: float = 0.1 # meters
    vertical_scale: float = 0.005 # meters
    border_size = 25 # [m]

    def __init__(self, num_robots, type, gym: gymapi.Gym, sim: gymapi.Sim, device: torch.device):
        if 'test' in type:
            self.num_rows = 5
            self.num_cols = 1
            self.terrain_width = 24.
        self.num_robots = num_robots
        self.num_envs = num_robots
        self.gym = gym
        self.sim = sim
        self.device = device
        self.actor_inds = None
        self.env_length = self.terrain_length
        self.env_width = self.terrain_width
        self.proportions = [np.sum(self.terrain_proportions[:i+1]) for i in range(len(self.terrain_proportions))]

        self.num_sub_terrains = self.num_rows * self.num_cols
        self.env_origins = np.zeros((self.num_rows, self.num_cols, 3))

        self.width_per_env_pixels = int(self.env_width / self.horizontal_scale)
        self.length_per_env_pixels = int(self.env_length / self.horizontal_scale)

        self.border = int(self.border_size/self.horizontal_scale)
        self.tot_cols = int(self.num_cols * self.width_per_env_pixels) + 2 * self.border
        self.tot_rows = int(self.num_rows * self.length_per_env_pixels) + 2 * self.border

        self.height_field_raw = np.zeros((self.tot_rows , self.tot_cols), dtype=np.int16)
        if type == 'curiculum':
            self.curiculum()
        else:
            self.test_terrain()
        
        self.heightsamples = self.height_field_raw
        self.vertices, self.triangles = tu.convert_heightfield_to_trimesh(self.height_field_raw,
                                                                        self.horizontal_scale,
                                                                        self.vertical_scale,
                                                                        self.slope_treshold)
        self.create_trimesh()
        y = torch.tensor(self.measured_points_y, device=self.device, requires_grad=False)
        x = torch.tensor(self.measured_points_x, device=self.device, requires_grad=False)
        grid_x, grid_y = torch.meshgrid(x, y)

        self.num_height_points = grid_x.numel()
        points = torch.zeros(self.num_envs, self.num_height_points, 3, device=self.device, requires_grad=False)
        points[:, :, 0] = grid_x.flatten()
        points[:, :, 1] = grid_y.flatten()
        self.points = points
        self._quat = torch.zeros((self.num_envs, 4), device=device)
        self.obs_space = Box(-np.inf, np.inf, (points.shape[1],))

    def set_actor_inds(self, actor_inds):
        self.actor_inds = actor_inds

    def create_trimesh(self):
        """ Adds a triangle mesh terrain to the simulation, sets parameters based on the cfg.
        # """
        tm_params = gymapi.TriangleMeshParams()
        tm_params.nb_vertices = self.vertices.shape[0]
        tm_params.nb_triangles = self.triangles.shape[0]

        tm_params.transform.p.x = -self.border_size 
        tm_params.transform.p.y = -self.border_size
        tm_params.transform.p.z = 0.0
        tm_params.static_friction = self.static_friction
        tm_params.dynamic_friction = self.dynamic_friction
        tm_params.restitution = self.restitution
        self.gym.add_triangle_mesh(self.sim, self.vertices.flatten(order='C'), self.triangles.flatten(order='C'), tm_params)   
        self.height_samples = torch.tensor(self.heightsamples).view(self.tot_rows, self.tot_cols).to(self.device)

    def __call__(self, tensor_api):
        heights = self.get_heights(tensor_api)
        # print(heights)
        return heights

    def get_heights(self, tensor_api):
        """ Samples heights of the terrain at required points around each robot.
            The points are offset by the base's position and rotated by the base's yaw

        Args:
            env_ids (List[int], optional): Subset of environments for which to return the heights. Defaults to None.

        Raises:
            NameError: [description]

        Returns:
            [type]: [description]
        """

        self._quat[..., 0:1] = tensor_api.actor_root_state.orientation[self.actor_inds, 3:4]
        self._quat[..., 3:4] = tensor_api.actor_root_state.orientation[self.actor_inds, 2:3]
        self._quat /= torch.norm(self._quat, p=2, dim=-1, keepdim=True)
        # apply yaw rotation
        points = transforms.quaternion_apply(self._quat.unsqueeze(1), self.points)[..., :2]
        # translate into world frame
        points += tensor_api.actor_root_state.position.unsqueeze(1)[self.actor_inds, :, :2]

        points += self.border_size
        points = (points/self.horizontal_scale).long()
        px = points[:, :, 0].view(-1)
        py = points[:, :, 1].view(-1)
        px = torch.clip(px, 0, self.height_samples.shape[0]-2)
        py = torch.clip(py, 0, self.height_samples.shape[1]-2)

        heights1 = self.height_samples[px, py]
        heights2 = self.height_samples[px+1, py]
        heights3 = self.height_samples[px, py+1]
        heights = torch.min(heights1, heights2)
        heights = torch.min(heights, heights3)

        return heights.view(self.num_robots, -1) * self.vertical_scale

    
    def randomized_terrain(self):
        for k in range(self.num_sub_terrains):
            # Env coordinates in the world
            (i, j) = np.unravel_index(k, (self.num_rows, self.num_cols))

            choice = np.random.uniform(0, 1)
            difficulty = np.random.choice([0.5, 0.75, 0.9])
            terrain = self.make_terrain(choice, difficulty)
            self.add_terrain_to_map(terrain, i, j)

    def test_terrain(self):
        for k in range(self.num_sub_terrains):
            # Env coordinates in the world
            (i, j) = np.unravel_index(k, (self.num_rows, self.num_cols))
            terrain = self.make_test_terrain(k, 0.5)
            self.add_terrain_to_map(terrain, i, j)
        
    def curiculum(self):
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                difficulty = i / self.num_rows
                choice = j / self.num_cols + 0.001

                terrain = self.make_terrain(choice, difficulty)
                self.add_terrain_to_map(terrain, i, j)   

    def plain(self):
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                terrain = tu.SubTerrain(   "terrain",
                                width=self.length_per_env_pixels,
                                length=self.width_per_env_pixels,
                                vertical_scale=self.vertical_scale,
                                horizontal_scale=self.horizontal_scale)
                self.add_terrain_to_map(terrain, i, j) 

    def lane(self, test=False):
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                terrain = tu.SubTerrain(   "terrain",
                                width=self.length_per_env_pixels,
                                length=self.width_per_env_pixels,
                                vertical_scale=self.vertical_scale,
                                horizontal_scale=self.horizontal_scale)   
                lane_terrain(terrain, lane_width=1, test=test)
                self.add_lane_terrain_to_map(terrain, i, j)

    def make_test_terrain(self, index, difficulty):
        terrain = tu.SubTerrain(   "terrain",
                                width=self.length_per_env_pixels,
                                length=self.width_per_env_pixels,
                                vertical_scale=self.vertical_scale,
                                horizontal_scale=self.horizontal_scale)
        slope = difficulty * 0.4
        step_height = 0.05 + 0.1 * difficulty
        discrete_obstacles_height = 0.05 + difficulty * 0.1
        stepping_stones_size = 1.5 * (1.05 - difficulty)
        stone_distance = 0.05 if difficulty==0 else 0.1
        gap_size = 1. * difficulty
        pit_depth = 1. * difficulty
        if index == 0:
            tu.random_uniform_terrain(terrain, min_height=-0.05, max_height=0.05, step=0.005, downsampled_scale=0.2)
        elif index == 1:
            step_height *= -1
            tu.pyramid_stairs_terrain(terrain, step_width=0.31, step_height=step_height, platform_size=3.)
        elif index == 2:
            tu.wave_terrain(terrain, num_waves=4, amplitude=0.15)
        elif index == 3:
            tu.pyramid_stairs_terrain(terrain, step_width=0.31, step_height=step_height, platform_size=3.)
        elif index == 4:
            num_rectangles = 50
            rectangle_min_size = 1.
            rectangle_max_size = 2.
            tu.discrete_obstacles_terrain(terrain, discrete_obstacles_height, rectangle_min_size, rectangle_max_size, num_rectangles, platform_size=3.)
        elif index == 4:
            tu.stepping_stones_terrain(terrain, stone_size=stepping_stones_size, stone_distance=stone_distance, max_height=0., platform_size=4.)
        elif index == 5:
            gap_terrain(terrain, gap_size=gap_size, platform_size=3.)
        else:
            pit_terrain(terrain, depth=pit_depth, platform_size=4.)
        
        return terrain
    
    def make_terrain(self, choice, difficulty):
        terrain = tu.SubTerrain(   "terrain",
                                width=self.length_per_env_pixels,
                                length=self.width_per_env_pixels,
                                vertical_scale=self.vertical_scale,
                                horizontal_scale=self.horizontal_scale)
        slope = difficulty * 0.4
        step_height = 0.05 + 0.1 * difficulty
        discrete_obstacles_height = 0.05 + difficulty * 0.1
        stepping_stones_size = 1.5 * (1.05 - difficulty)
        stone_distance = 0.05 if difficulty==0 else 0.1
        gap_size = 1. * difficulty
        pit_depth = 1. * difficulty
        if choice < self.proportions[0]:
            if choice < self.proportions[0]/ 2:
                slope *= -1
            tu.pyramid_sloped_terrain(terrain, slope=slope, platform_size=3.)
        elif choice < self.proportions[1]:
            tu.pyramid_sloped_terrain(terrain, slope=slope, platform_size=3.)
            tu.random_uniform_terrain(terrain, min_height=-0.05, max_height=0.05, step=0.005, downsampled_scale=0.2)
        elif choice < self.proportions[3]:
            if choice<self.proportions[2]:
                step_height *= -1
            tu.pyramid_stairs_terrain(terrain, step_width=0.31, step_height=step_height, platform_size=3.)
        elif choice < self.proportions[4]:
            num_rectangles = 20
            rectangle_min_size = 1.
            rectangle_max_size = 2.
            tu.discrete_obstacles_terrain(terrain, discrete_obstacles_height, rectangle_min_size, rectangle_max_size, num_rectangles, platform_size=3.)
        elif choice < self.proportions[5]:
            tu.stepping_stones_terrain(terrain, stone_size=stepping_stones_size, stone_distance=stone_distance, max_height=0., platform_size=4.)
        elif choice < self.proportions[6]:
            gap_terrain(terrain, gap_size=gap_size, platform_size=3.)
        else:
            pit_terrain(terrain, depth=pit_depth, platform_size=4.)
        
        return terrain

    def add_terrain_to_map(self, terrain, row, col):
        i = row
        j = col
        # map coordinate system
        start_x = self.border + i * self.length_per_env_pixels
        end_x = self.border + (i + 1) * self.length_per_env_pixels
        start_y = self.border + j * self.width_per_env_pixels
        end_y = self.border + (j + 1) * self.width_per_env_pixels
        self.height_field_raw[start_x: end_x, start_y:end_y] = terrain.height_field_raw

        env_origin_x = (i + 0.5) * self.env_length
        env_origin_y = (j + 0.5) * self.env_width
        x1 = int((self.env_length/2. - 1) / terrain.horizontal_scale)
        x2 = int((self.env_length/2. + 1) / terrain.horizontal_scale)
        y1 = int((self.env_width/2. - 1) / terrain.horizontal_scale)
        y2 = int((self.env_width/2. + 1) / terrain.horizontal_scale)
        env_origin_z = np.max(terrain.height_field_raw[x1:x2, y1:y2])*terrain.vertical_scale
        self.env_origins[i, j] = [env_origin_x, env_origin_y, env_origin_z]

    def add_lane_terrain_to_map(self, terrain, row, col):
        i = row
        j = col
        # map coordinate system
        start_x = self.border + i * self.length_per_env_pixels
        end_x = self.border + (i + 1) * self.length_per_env_pixels
        start_y = self.border + j * self.width_per_env_pixels
        end_y = self.border + (j + 1) * self.width_per_env_pixels
        self.height_field_raw[start_x: end_x, start_y:end_y] = terrain.height_field_raw

        env_origin_x = i * self.env_length + 1
        env_origin_y = (j + 0.5) * self.env_width
        env_origin_z = 0
        self.env_origins[i, j] = [env_origin_x, env_origin_y, env_origin_z]

def lane_terrain(terrain, lane_width=1, test=False):
    lane_width = int(lane_width / terrain.horizontal_scale)
    if test:
        x1 = 0
    else:
        x1 = int(2. / terrain.horizontal_scale)
    y1 = (terrain.height_field_raw.shape[1] - lane_width) // 2
    y2 = (terrain.height_field_raw.shape[1] + lane_width) // 2
    terrain.height_field_raw[x1:,:y1] = 400
    terrain.height_field_raw[x1:,y2:] = 400
    terrain.height_field_raw[x1:,y1:y2] = 0

def gap_terrain(terrain, gap_size, platform_size=1.):
    gap_size = int(gap_size / terrain.horizontal_scale)
    platform_size = int(platform_size / terrain.horizontal_scale)

    center_x = terrain.length // 2
    center_y = terrain.width // 2
    x1 = (terrain.length - platform_size) // 2
    x2 = x1 + gap_size
    y1 = (terrain.width - platform_size) // 2
    y2 = y1 + gap_size
   
    terrain.height_field_raw[center_x-x2 : center_x + x2, center_y-y2 : center_y + y2] = -1000
    terrain.height_field_raw[center_x-x1 : center_x + x1, center_y-y1 : center_y + y1] = 0

def pit_terrain(terrain, depth, platform_size=1.):
    depth = int(depth / terrain.vertical_scale)
    platform_size = int(platform_size / terrain.horizontal_scale / 2)
    x1 = terrain.length // 2 - platform_size
    x2 = terrain.length // 2 + platform_size
    y1 = terrain.width // 2 - platform_size
    y2 = terrain.width // 2 + platform_size
    terrain.height_field_raw[x1:x2, y1:y2] = -depth