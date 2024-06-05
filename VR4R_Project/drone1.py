import setup_path
import airsim
from drone_controller import DroneController
from astar_algorithm import load_grid_from_csv

def main():
    client = airsim.MultirotorClient()

    # Load map and waypoints for Drone1
    map_data = load_grid_from_csv('map1.csv')
    home = (0, 0)
    waypoints = [(40, -15), (10, -7), (45, -15), (15, 2)]
    target_altitude = -5
    obstacle_threshold = 4

    controller = DroneController(client, "Drone1", home, waypoints, map_data, target_altitude, obstacle_threshold)
    controller.run()

if __name__ == "__main__":
    main()
