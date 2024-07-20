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
import trimesh

@dataclasses.dataclass
class Terrain():
    num_envs: int
    spacing: Sequence[float]
    num_per_row: int
    static_friction: float = 1.0
    dynamic_friction: float = 1.0
    restitution: float = 0.0
    x_border: float = 2.0
    y_border: float = 20.0

    def create(self, gym: gymapi.Gym, sim: gymapi.Sim):
        raise NotImplementedError

    def get_heights(self, points: torch.Tensor):
        """ points is an (... x 2) tensor """
        raise NotImplementedError

    def get_init_bounds(self):
        num_per_col = int(np.ceil(self.num_envs / self.num_per_row))
        low = -np.array(self.spacing)
        high = np.array([
                2 * self.spacing[0] * self.num_per_row - self.spacing[0],
                2 * self.spacing[1] * num_per_col - self.spacing[1],
                self.spacing[2]
            ])
        low[0] -= self.x_border
        low[1] -= self.y_border
        high[0] += self.x_border
        high[1] += self.y_border
        return low, high

    def get_terrain_bounds(self):
        raise NotImplementedError


@dataclasses.dataclass
class HeightFieldTerrain(Terrain):
    horizontal_scale: float = 0.1 # meters
    vertical_scale: float = 0.005 # meters

    def _get_terrain(self, num_rows, num_cols):
        return tu.SubTerrain(width=num_rows, length=num_cols,
                             vertical_scale=self.vertical_scale,
                             horizontal_scale=self.horizontal_scale)

    def _convert_heightfield_to_mesh(self, heightfield):
        vertices, triangles = tu.convert_heightfield_to_trimesh(
                heightfield, self.horizontal_scale, self.vertical_scale,
                slope_threshold=0.75)
        low, _ = self.get_init_bounds()
        params = gymapi.TriangleMeshParams()
        params.static_friction = self.static_friction
        params.dynamic_friction = self.dynamic_friction
        params.restitution = self.restitution
        params.nb_vertices = vertices.shape[0]
        params.nb_triangles = triangles.shape[0]
        params.transform.p.x = low[0]
        params.transform.p.y = low[1]

        return vertices, triangles, params

    def set_heightfield(self, gym: gymapi.Gym, sim: gymapi.Sim, heightfield: np.ndarray):
        self.heights = torch.from_numpy(heightfield).float() * self.vertical_scale
        vertices, triangles, params = self._convert_heightfield_to_mesh(heightfield)
        self.low = torch.tensor([params.transform.p.x, params.transform.p.y])
        self.high = self.low + (torch.tensor(self.heights.shape) - 1) * self.horizontal_scale
        self.size = self.high - self.low
        self.shape = torch.tensor(self.heights.shape)
        self.params = params
        gym.add_triangle_mesh(sim, vertices.flatten(), triangles.flatten(), params)

    def get_heights(self, points: torch.Tensor):
        if not hasattr(self, 'heights'):
            raise RuntimeError('Call set_heightfield before get_heights')
        if points.device != self.heights.device:
            self.heights = self.heights.to(points.device)
            self.low = self.low.to(points.device)
            self.high = self.high.to(points.device)
            self.size = self.size.to(points.device)
            self.shape = self.shape.to(points.device)
        inds = ((points.clamp(self.low, self.high) - self.low) / self.size * self.shape).long()
        inds = torch.clamp(inds, max=self.shape - 2)
        h1 = self.heights[inds[..., 0], inds[..., 1]]
        h2 = self.heights[inds[..., 0]+1, inds[..., 1]+1]
        # The min is needed here because of how isaacgym.tu handles slope thresholds
        return torch.min(h1, h2)

    def get_terrain_bounds(self):
        if not hasattr(self, 'heights'):
            return None
        x, y = self.shape
        low_x = self.params.transform.p.x
        low_y = self.params.transform.p.y
        high_x = low_x + x * self.horizontal_scale
        high_y = low_y + y * self.horizontal_scale
        return (low_x, high_x), (low_y, high_y)

    def create(self, gym: gymapi.Gym, sim: gymapi.Sim):
        self.set_heightfield(gym, sim, self.build_heightfield())

    def build_heightfield(self):
        raise NotImplementedError


@gin.configurable(module='terrain')
class TerrainIndexer():
    def __init__(self, gym: gymapi.Gym, sim: gymapi.Sim, device: torch.device, terrain: Terrain,
                 actor_inds: torch.Tensor,
                 x_pos = [-.8, -.7, -.6, -.5, -.4, -.3, -.2, .2, .3, .4, .5, .6, .7, .8],
                 y_pos = [-.5, -.4, -.3, -.2, -.1, .1, .2, .3, .4, .5]):
        self.gym = gym
        self.sim = sim
        self.device = device
        self.num_envs = gym.get_env_count(sim)
        self.terrain = terrain
        self.actor_inds = actor_inds
        x_pos = torch.tensor(x_pos, device=device)
        y_pos = torch.tensor(y_pos, device=device)
        grid_x, grid_y = torch.meshgrid(x_pos, y_pos)
        self.num_height_points = grid_x.numel()
        self.points = torch.zeros((self.num_envs, grid_x.numel(), 3), device=device)
        self.points[..., 0] = grid_x.flatten()
        self.points[..., 1] = grid_y.flatten()
        origins = [
            gym.get_env_origin(gym.get_env(sim, i)) for i in range(self.num_envs)
        ] # origins of each env
        self.origins = torch.tensor([[o.x, o.y] for o in origins], device=device)
        self._quat = torch.zeros((self.num_envs, 4), device=device)
        self.obs_space = Box(-np.inf, np.inf, (self.points.shape[1],))

    def __call__(self, tensor_api):
        # get yaw rotation
        self._quat[..., 0:1] = tensor_api.actor_root_state.orientation[self.actor_inds, 3:4]
        self._quat[..., 3:4] = tensor_api.actor_root_state.orientation[self.actor_inds, 2:3]
        self._quat /= torch.norm(self._quat, p=2, dim=-1, keepdim=True)
        # apply yaw rotation
        points = transforms.quaternion_apply(self._quat.unsqueeze(1), self.points)[..., :2]
        # translate into world frame
        points += tensor_api.actor_root_state.position.unsqueeze(1)[self.actor_inds, :, :2]
        points += self.origins.unsqueeze(1)
        # get heights
        return self.terrain.get_heights(points)



@gin.configurable(module='terrain')
@dataclasses.dataclass
class FlatTerrain(Terrain):
    def create(self, gym: gymapi.Gym, sim: gymapi.Sim):
        self.plane_params = gymapi.PlaneParams()
        self.plane_params.normal = gymapi.Vec3(0.0, 0.0, 1.0)
        self.plane_params.static_friction = self.static_friction
        self.plane_params.dynamic_friction = self.dynamic_friction
        self.plane_params.restitution = self.restitution
        gym.add_ground(sim, self.plane_params)

    def get_heights(self, points):
        return torch.zeros_like(points[..., 0])

    def get_terrain_bounds(self):
        return None


@gin.configurable(module='terrain')
@dataclasses.dataclass
class StairsTerrain(HeightFieldTerrain):
    length: float = 50.0 # meters
    stair_height: float = 0.1 # meters
    stair_width: float = 0.5 # meters

    def build_heightfield(self):
        low, high = self.get_init_bounds()
        size = (high - low)
        num_stair_rows = int(self.length // self.horizontal_scale)
        num_flat_rows = int(size[0] // self.horizontal_scale)
        num_cols = int(size[1] // self.horizontal_scale)
        heightfield = np.zeros((num_stair_rows + num_flat_rows, num_cols), dtype=np.int16)

        stairs = self._get_terrain(num_stair_rows, num_cols)
        heightfield[num_flat_rows:, :] = tu.stairs_terrain(
                stairs,
                step_width=self.stair_width,
                step_height=self.stair_height
        ).height_field_raw
        return heightfield


@gin.configurable(module='terrain')
@dataclasses.dataclass
class RandomStairsTerrain(HeightFieldTerrain):
    length: float = 50.0 # meters
    stair_height_min: float = 0.05 # meters
    stair_height_max: float = 0.15 # meters
    stair_width_min: float = 0.5 # meters
    stair_width_max: float = 1.0 # meters
    ramp_up_steps: int = 10
    up: bool = True
    include_starting_area: bool = True
    initial_height: float = 0.0

    def build_heightfield(self):
        low, high = self.get_init_bounds()
        size = (high - low)

        step_hmax = int(self.stair_height_max // self.vertical_scale)
        step_hmin = int(self.stair_height_min // self.vertical_scale)
        step_wmax = int(self.stair_width_max // self.horizontal_scale)
        step_wmin = int(self.stair_width_min // self.horizontal_scale)

        num_stair_rows = int(self.length // self.horizontal_scale)
        if self.include_starting_area:
            num_flat_rows = int(size[0] // self.horizontal_scale)
        else:
            num_flat_rows = 0
        num_cols = int(size[1] // self.horizontal_scale)
        heightfield = np.zeros((num_stair_rows + num_flat_rows, num_cols), dtype=np.int16)


        rows_used = 0
        steps = 0
        height = self.initial_height
        while rows_used < num_stair_rows:
            step_width = min(num_stair_rows - rows_used, random.randint(step_wmin, step_wmax))
            step_width = max(step_width, 2)
            hmin = int(min(1, (steps / self.ramp_up_steps)) * step_hmin)
            hmax = int(min(1, (steps / self.ramp_up_steps)) * step_hmax)
            step_height = random.randint(hmin, hmax)
            if self.up:
                height += step_height
            else:
                height -= step_height
            heightfield[num_flat_rows + rows_used:num_flat_rows + rows_used + step_width] = height
            rows_used += step_width
            steps += 1
        return heightfield


@gin.configurable(module='terrain')
@dataclasses.dataclass
class RandomWallsTerrain(HeightFieldTerrain):
    length: float = 50.0 # meters
    wall_height_min: float = 0.5 # meters
    wall_height_max: float = 1.0 # meters
    wall_distance_min: float = 2.0 # meters
    wall_distance_max: float = 3.0 # meters
    wall_thickness: float = 0.5 # meters
    ramp_up_steps: int = 10
    include_starting_area: bool = True
    initial_height: float = 0.0

    def build_heightfield(self):
        low, high = self.get_init_bounds()
        size = (high - low)

        wall_hmax = int(self.wall_height_max // self.vertical_scale)
        wall_hmin = int(self.wall_height_min // self.vertical_scale)
        wall_dmax = int(self.wall_distance_max // self.horizontal_scale)
        wall_dmin = int(self.wall_distance_min // self.horizontal_scale)
        wall_thickness = int(self.wall_thickness // self.horizontal_scale)

        num_wall_rows = int(self.length // self.horizontal_scale)
        if self.include_starting_area:
            num_flat_rows = int(size[0] // self.horizontal_scale)
        else:
            num_flat_rows = 0
        num_cols = int(size[1] // self.horizontal_scale)
        heightfield = self.initial_height * np.ones((num_wall_rows + num_flat_rows, num_cols), dtype=np.int16)

        rows_used = 0
        steps = 0
        while rows_used < num_wall_rows:
            wall_dist = random.randint(wall_dmin, wall_dmax)
            rows_used += wall_dist
            if rows_used >= num_wall_rows:
                break
            hmin = int(min(1, (steps / self.ramp_up_steps)) * wall_hmin)
            hmax = int(min(1, (steps / self.ramp_up_steps)) * wall_hmax)
            height = random.randint(hmin, hmax)

            heightfield[num_flat_rows + rows_used:num_flat_rows + rows_used + wall_thickness] = self.initial_height + height
            rows_used += wall_thickness
            steps += 1
        return heightfield


@gin.configurable(module='terrain')
@dataclasses.dataclass
class RandomGapsTerrain(HeightFieldTerrain):
    length: float = 50.0 # meters
    gap_min: float = 0.25 # meters
    gap_max: float = 1.0 # meters
    gap_distance_min: float = 1.0 # meters
    gap_distance_max: float = 3.0 # meters
    gap_height: float = -3.0 # meters
    ramp_up_steps: int = 5
    include_starting_area: bool = True
    initial_height: float = 0.0

    def build_heightfield(self):
        low, high = self.get_init_bounds()
        size = (high - low)

        gap_max = int(self.gap_max // self.horizontal_scale)
        gap_min = int(self.gap_min // self.horizontal_scale)
        gap_dmax = int(self.gap_distance_max // self.horizontal_scale)
        gap_dmin = int(self.gap_distance_min // self.horizontal_scale)
        gap_height = int(self.gap_height // self.vertical_scale)

        num_gap_rows = int(self.length // self.horizontal_scale)
        if self.include_starting_area:
            num_flat_rows = int(size[0] // self.horizontal_scale)
        else:
            num_flat_rows = 0
        num_cols = int(size[1] // self.horizontal_scale)
        heightfield = self.initial_height * np.ones((num_gap_rows + num_flat_rows, num_cols), dtype=np.int16)


        rows_used = 0
        steps = 0
        while rows_used < num_gap_rows:
            gap_dist = random.randint(gap_dmin, gap_dmax)
            rows_used += gap_dist
            if rows_used >= num_gap_rows:
                break
            wmin = int(min(1, (steps / self.ramp_up_steps)) * gap_min)
            wmax = int(min(1, (steps / self.ramp_up_steps)) * gap_max)
            gap_w = random.randint(wmin, wmax)
            heightfield[num_flat_rows + rows_used:num_flat_rows + rows_used + gap_w] = gap_height
            rows_used += gap_w
            steps += 1

        return heightfield
    

@gin.configurable(module='terrain')
@dataclasses.dataclass
class WaveTerrain(HeightFieldTerrain):
    length: float = 50.0 # meters
    amplitude: float = 0.3 # meters
    num_waves: int = 5
    include_starting_area: bool = True
    initial_height: float = 0.0

    def build_heightfield(self):
        low, high = self.get_init_bounds()
        size = (high - low)
        num_wave_rows = int(self.length // self.horizontal_scale)
        if self.include_starting_area:
            num_flat_rows = int(size[0] // self.horizontal_scale)
        else:
            num_flat_rows = 0
        num_cols = int(size[1] // self.horizontal_scale)
        heightfield = self.initial_height * np.ones((num_wave_rows + num_flat_rows, num_cols), dtype=np.int16)

        terrain = self._get_terrain(num_wave_rows, num_cols)
        heightfield[num_flat_rows:, :] = self.initial_height + tu.wave_terrain(
                terrain,
                amplitude=self.amplitude,
                num_waves=self.num_waves
        ).height_field_raw
        return heightfield


@gin.configurable(module='terrain')
@dataclasses.dataclass
class RandomTerrain(HeightFieldTerrain):
    length: float = 20.0 # meters

    def build_heightfield(self):
        terrains = [RandomStairsTerrain, WaveTerrain,
                    RandomGapsTerrain, RandomWallsTerrain]
        random.shuffle(terrains)
        up_stairs = True
        heightfields = []
        initial_height = 0
        for i, terr in enumerate(terrains):
            if terr == RandomStairsTerrain:
                t = terr(num_envs=self.num_envs,
                         spacing=self.spacing,
                         num_per_row=self.num_per_row,
                         length=self.length,
                         up=up_stairs,
                         include_starting_area=i==0,
                         initial_height=initial_height)
                heightfields.append(t.build_heightfield())
                initial_height = heightfields[-1][-1, 0]
                up_stairs = False
            else:
                t = terr(num_envs=self.num_envs,
                         spacing=self.spacing,
                         num_per_row=self.num_per_row,
                         length=self.length,
                         include_starting_area=i==0,
                         initial_height=initial_height)
                heightfields.append(t.build_heightfield())

        return np.concatenate(heightfields, axis=0)
    


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
        if type != 'curiculum':
            self.num_rows = 5
            self.num_cols = 1
            self.terrain_width = 16.
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

    def create_trimesh_from_obj(self,file_path):
        mesh = trimesh.load(file_path)
        vertices = np.array(mesh.vertices, dtype=np.float32)
        faces = np.array(mesh.faces, dtype=np.int32)
        """ Adds a triangle mesh terrain to the simulation, data from obj
        # """
        tm_params = gymapi.TriangleMeshParams()
        tm_params.nb_vertices = vertices.shape[0]
        tm_params.nb_triangles = faces.shape[0]

        tm_params.transform.p.x = -self.border_size 
        tm_params.transform.p.y = -self.border_size
        tm_params.transform.p.z = 0.0
        tm_params.static_friction = self.static_friction
        tm_params.dynamic_friction = self.dynamic_friction
        tm_params.restitution = self.restitution
        self.gym.add_triangle_mesh(self.sim, vertices.flatten(order='C'), faces.flatten(order='C'), tm_params)   
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


def add_low_height_bridge(terrain, bridge_height=2, bridge_length=10, bridge_width=5, platform_height=0):
    bridge_height = int(bridge_height / terrain.vertical_scale)
    bridge_length = int(bridge_length / terrain.horizontal_scale)
    bridge_width = int(bridge_width / terrain.horizontal_scale)
    platform_height = int(platform_height / terrain.vertical_scale)

    center_x = terrain.length // 2
    center_y = terrain.width // 2
    x1 = center_x - bridge_length // 2
    x2 = center_x + bridge_length // 2
    y1 = center_y - bridge_width // 2
    y2 = center_y + bridge_width // 2

    # Set the height of the bridge area
    terrain.height_field_raw[x1:x2, y1:y2] = bridge_height

    # Optional: Set the platform height underneath the bridge
    if platform_height != 0:
        terrain.height_field_raw[x1:x2, y1:y2] = platform_height

def add_narrow_passage(terrain, wall_height=5, wall_thickness=1, passage_width=3):
    wall_height = int(wall_height / terrain.vertical_scale)
    wall_thickness = int(wall_thickness / terrain.horizontal_scale)
    passage_width = int(passage_width / terrain.horizontal_scale)

    center_x = terrain.length // 2
    center_y = terrain.width // 2

    # Calculate the starting and ending points for the passage and walls
    total_half_width = (passage_width + 2 * wall_thickness) // 2
    passage_start_y = center_y - passage_width // 2
    passage_end_y = passage_start_y + passage_width

    wall1_start_y = passage_start_y - wall_thickness
    wall1_end_y = passage_start_y
    wall2_start_y = passage_end_y
    wall2_end_y = passage_end_y + wall_thickness

    # Ensure the walls do not go out of bounds
    if wall1_start_y < 0:
        wall1_start_y = 0
    if wall2_end_y > terrain.width:
        wall2_end_y = terrain.width

    # Set the height of the walls
    terrain.height_field_raw[:, wall1_start_y:wall1_end_y] = wall_height
    terrain.height_field_raw[:, wall2_start_y:wall2_end_y] = wall_height


