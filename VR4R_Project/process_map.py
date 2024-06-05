import csv

# Initialize dictionaries to store the values for each map
map1 = {}
map2 = {}
map3 = {}

def mark_neighbors_as_obstacles(grid, x, y):
    """
    Mark neighbors of a grid cell as obstacles if their height exceeds a threshold.

    Args:
        grid (dict): Dictionary representing the grid.
        x (int): X-coordinate of the grid cell.
        y (int): Y-coordinate of the grid cell.
    """
    # Define the 8 possible neighbor directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        # Check if the neighbor is within grid bounds and if its height exceeds the threshold
        if neighbor in grid and grid[neighbor] <= 5:
            grid[neighbor] = 6  # Mark as an obstacle

# Read the map data from the CSV file and populate the maps accordingly
with open('map.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for y, row in enumerate(csvreader):
        for x, value in enumerate(row):
            value = int(value)
            # Determine which map the grid cell belongs to based on its y-coordinate
            if y <= 20:
                map1[(x - 3, y - 18)] = value
            elif 21 <= y <= 31:
                map2[(x - 3, y - 25)] = value
            else:
                map3[(x - 3, y - 32)] = value

# Process each map and mark neighbors as obstacles
for map_data in [map1, map2, map3]:
    obstacle_positions = [key for key, value in map_data.items() if value > 5]
    for x, y in obstacle_positions:
        mark_neighbors_as_obstacles(map_data, x, y)

def write_to_csv(map_data, filename):
    """
    Write map data to a CSV file.

    Args:
        map_data (dict): Dictionary representing the map data.
        filename (str): Name of the output CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in map_data.items():
            writer.writerow([key[0], key[1], value])

# Write each map data to a separate CSV file
write_to_csv(map1, 'map1.csv')
write_to_csv(map2, 'map2.csv')
write_to_csv(map3, 'map3.csv')

print("Output written to CSV files.")
