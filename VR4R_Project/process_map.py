import csv

# Initialize dictionaries to store the values
map1 = {}
map2 = {}
map3 = {}

# Function to mark neighbors as obstacles
def mark_neighbors_as_obstacles(grid, x, y):
    # Define the 8 possible neighbor directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in grid and grid[neighbor] <= 5:
            grid[neighbor] = 6  # Mark as obstacle with height greater than 5

# Open the CSV file for reading
with open('map.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for y, row in enumerate(csvreader):
        # Iterate over each value in the row
        for x, value in enumerate(row):
            # Convert the value to the appropriate data type if needed
            value = int(value)  # Assuming values are integers

            if y <= 20:
                 map1[(x - 3, y - 18)] = value
            elif 21 <= y <= 31:
                map2[(x - 3, y - 25)] = value
            else:
                map3[(x - 3, y - 32)] = value

# Function to process each map and mark neighbors as obstacles
def process_map(map_data):
    obstacle_positions = [key for key, value in map_data.items() if value > 5]
    for x, y in obstacle_positions:
        mark_neighbors_as_obstacles(map_data, x, y)

# Process each map
process_map(map1)
process_map(map2)
process_map(map3)

# Write map1 data to a CSV file
with open('map1.csv', 'w', newline='') as csvfile:
    for key, value in map1.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

# Write map2 data to a CSV file
with open('map2.csv', 'w', newline='') as csvfile:
    for key, value in map2.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

# Write map3 data to a CSV file
with open('map3.csv', 'w', newline='') as csvfile:
    for key, value in map3.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

print("Output written to CSV files.")