from binvox_rw import read_as_3d_array
import matplotlib.pyplot as plt
import numpy as np

##https://github.com/microsoft/AirSim/issues/4810

with open('new_map.binvox', 'rb') as f:
    model = read_as_3d_array(f)
voxels = model.data

# Plot a slice of the voxel data (XY plane)
slice_index = voxels.shape[2] // 2 
plt.figure(figsize=(20, 20))
plt.imshow(voxels[:, :, slice_index], cmap='binary', origin='lower')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Top-Down View of Blocks Environment (Slice)')
plt.grid(True)
plt.show()


