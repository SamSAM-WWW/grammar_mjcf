import trimesh
import numpy as np

def load_obj_mesh(file_path):
    """
    Load an OBJ file and return vertices and faces in the format used by convert_heightfield_to_trimesh.

    Parameters:
        file_path (str): Path to the OBJ file.

    Returns:
        vertices (np.array): Array of shape (num_vertices, 3). Each row represents the location of each vertex.
        faces (np.array): Array of shape (num_faces, 3). Each row represents the indices of the 3 vertices connected by this face.
    """
    # Load mesh using trimesh
    mesh = trimesh.load(file_path)
    vertices = np.array(mesh.vertices, dtype=np.float32)
    faces = np.array(mesh.faces, dtype=np.int32)
    
    return vertices, faces


if __name__ == '__main__':
    vertices,faces = load_obj_mesh("D:\pythoncode\\bridge.obj")
    print(vertices)
    print(vertices.shape[0])
    print(faces)
    print(faces.shape[0])
# # Initialize gym and sim
# gym = gymapi.acquire_gym()
# sim_params = gymapi.SimParams()
# sim = gym.create_sim(0, 0, gymapi.SIM_PHYSX, sim_params)

# # Create mesh geometry and add it to the environment
# file_path = "path_to_your_obj_file.obj"
# mesh_asset = create_mesh_geometry(gym, sim, file_path)

# # Create an environment and add the mesh asset to it
# env = gym.create_env(sim, gymapi.Vec3(-5, -5, -5), gymapi.Vec3(5, 5, 5), 1)
# pose = gymapi.Transform()
# gym.create_actor(env, mesh_asset, pose, "mesh", 0, 1)