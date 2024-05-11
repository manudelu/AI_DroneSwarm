import numpy as np
from binvox_rw import read_as_3d_array


def read_binvox(file_path):
    """
    Read binvox file and return voxel grid data.

    Args:
    - file_path: Path to the binvox file

    Returns:
    - voxel_data: Voxel grid data as numpy array
    - dims: Dimensions of the voxel grid
    """
    with open(file_path, 'rb') as f:
        # Read binvox data using binvox_rw
        binvox_model = read_as_3d_array(f)

        # Extract voxel data and dimensions from the binvox model
        voxel_data = binvox_model.data.astype(np.bool_)
        dims = binvox_model.dims

    return voxel_data, dims

def convert_to_occupancy_map(voxel_data):
    """
    Convert voxel grid data to a 3D occupancy map.

    Args:
    - voxel_data: Voxel grid data as numpy array

    Returns:
    - occupancy_map: 3D occupancy map as numpy array
    """
    # Create an empty occupancy map with the same dimensions as the voxel grid
    occupancy_map = np.zeros_like(voxel_data, dtype=np.bool_)

    # Assign 1 to occupied cells based on the voxel data
    occupancy_map[voxel_data] = 1

    return occupancy_map

def print_occupancy_map(occupancy_map):
    """
    Print the occupancy map.

    Args:
    - occupancy_map: 3D occupancy map as numpy array
    """
    with open ("plot.txt", "a") as file:
        for z in range(occupancy_map.shape[0]):
            for y in range(occupancy_map.shape[1]):
                for x in range(occupancy_map.shape[2]):
                    if occupancy_map[z, y, x]: 
                        file.write("#")
                    else:
                        file.write(".")
                file.write("\n")
            file.write(" ")

# Example usage
if __name__ == "__main__":
    # Read binvox file
    file_path = "new_map.binvox"  # Update with your actual file path
    voxel_data, dims = read_binvox(file_path)

    # Convert voxel grid data to occupancy map
    occupancy_map = convert_to_occupancy_map(voxel_data)

    # Print the occupancy map
    print_occupancy_map(occupancy_map)
