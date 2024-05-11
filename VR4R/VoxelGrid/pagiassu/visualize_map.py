import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

def plot_3d_map(voxel_data):
    """
    Plot the 3D map.

    Args:
    - voxel_data: Voxel grid data as numpy array
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract non-zero indices
    nz_indices = np.nonzero(voxel_data)

    # Plot non-zero voxels
    ax.scatter(nz_indices[0], nz_indices[1], nz_indices[2], c='b', marker='s')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Map')
    
    plt.show()

# Example usage
if __name__ == "__main__":
    # Read binvox file
    file_path = "map.binvox"  # Update with your actual file path
    voxel_data, dims = read_binvox(file_path)

    # Plot the 3D map
    plot_3d_map(voxel_data)
