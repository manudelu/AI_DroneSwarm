from binvox_rw import read_as_3d_array
import matplotlib.pyplot as plt
import numpy as np

# Create an empty occupancy map with the same dimensions as the voxel grid
#occupancy_map = np.zeros_like(voxel_data, dtype=np.bool_)

# Assign 1 to occupied cells based on the voxel data
#occupancy_map[voxel_data] = 1

counts_per_row = []

with open('plot.txt', 'r') as file:
    for line in file:
        # Count the occurrences of "#" in the line and append to the list
        count = line.count("#")
        counts_per_row.append(count)

# Now, print the counts of "#" in each row
x = 0
y = 0
for count in enumerate(counts_per_row, start=1):
    if x%250 == 0:
        y += 1
        x /= 250
    print(f"Row {x}, Column {y}: {count[1]}")
    x += 1


