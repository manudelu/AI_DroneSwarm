import setup_path
import airsim
import csv
import os

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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in grid and grid[neighbor] <= 5:
            grid[neighbor] = 6  # Mark as an obstacle

def read_map_data(csv_filename, home_positions):
    """
    Read the map data from the CSV file and populate the maps accordingly.

    Args:
        csv_filename (str): Name of the CSV file containing map data.
        home_positions (list): List of home positions of the drones.
    """
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for y, row in enumerate(csvreader):
            for x, value in enumerate(row):
                value = int(value)
                if y <= 20:
                    map1[(x - int(home_positions[0].position.x_val), y - int(home_positions[0].position.y_val))] = value
                elif 21 <= y <= 31:
                    map2[(x - int(home_positions[1].position.x_val), y - int(home_positions[1].position.y_val))] = value
                else:
                    map3[(x - int(home_positions[2].position.x_val), y - int(home_positions[2].position.y_val))] = value

def process_map_data(map_data):
    """
    Process the map data to mark neighbors as obstacles.

    Args:
        map_data (dict): Dictionary representing the map data.
    """
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
        for (x, y), value in sorted(map_data.items()):
            writer.writerow([x, y, value])

def main():
    try:
        client = airsim.MultirotorClient()
        home_positions = [
            client.simGetObjectPose("Drone1"),
            client.simGetObjectPose("Drone2"),
            client.simGetObjectPose("Drone3")
        ]

        # Read map data from CSV file
        read_map_data('map.csv', home_positions)

        # Process each map
        for map_data, filename in zip([map1, map2, map3], ['map1.csv', 'map2.csv', 'map3.csv']):
            process_map_data(map_data)
            write_to_csv(map_data, filename)

        print("Output written to CSV files.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
