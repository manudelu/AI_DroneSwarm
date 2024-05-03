import numpy as np
import binvox_rw

def convert_binvox_to_occupancy_grid(binvox_file_path, output_file_path):
    # Read the binvox file
    with open(binvox_file_path, 'rb') as f:
        binvox_model = binvox_rw.read_as_3d_array(f)

    # Extract necessary information from the binvox model
    dims = binvox_model.dims
    translate = binvox_model.translate
    scale = binvox_model.scale
    data = binvox_model.data

    # Convert the voxel data to a binary occupancy grid
    occupancy_grid = np.zeros(dims, dtype=bool)
    occupancy_grid[data[:, :, :]] = True

    # Flatten the 3D array to a 2D array
    flattened_grid = occupancy_grid.reshape(-1, dims[2])

    # Write the binary occupancy grid to a file
    np.savetxt(output_file_path, flattened_grid, fmt='%d', delimiter='')

if __name__ == "__main__":
    binvox_file_path = 'map.binvox'
    output_file_path = 'occupancy_grid.txt'
    convert_binvox_to_occupancy_grid(binvox_file_path, output_file_path)
