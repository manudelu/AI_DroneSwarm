import airsim
import os
import binvox_rw
import numpy as np
import csv

def binvox_generator():
    c = airsim.VehicleClient()
    center = airsim.Vector3r(0, 0, 0)
    output_path = os.path.join(os.getcwd(), "new_map.binvox")
    c.simCreateVoxelGrid(center, 56, 56, 56, 1, output_path)

# In order to visualize the .binvox install viewvox from this link: https://www.patrickmin.com/viewvox/

def create_map():
    # Load .binvox file
    def load_binvox(filename):
        with open(filename, 'rb') as f:
            binvox_model = binvox_rw.read_as_3d_array(f)
        return binvox_model.data

    # Extract 2.5D map data (top-down view)
    def extract_2_5D_map(binvox_data):
        # Sum along the z-axis to get 2D representation
        map_2D = np.sum(binvox_data, axis=2)
        return map_2D

    # Save 2.5D map data to CSV file
    def save_to_csv(data, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

    # Example usage
    if __name__ == "__main__":
        # Load .binvox file
        binvox_file = "map.binvox"
        binvox_data = load_binvox(binvox_file)
        
        # Extract 2.5D map data
        map_2D = extract_2_5D_map(binvox_data)
        
        # Save to CSV file
        csv_file = "map.csv"
        save_to_csv(map_2D, csv_file)

def separate_map():
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

                if y <= 21:
                    map1[(x, y)] = value
                elif 22 <= y <= 31:
                    map2[(x, y - 22)] = value
                else:
                    map3[(x, y - 32)] = value

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

