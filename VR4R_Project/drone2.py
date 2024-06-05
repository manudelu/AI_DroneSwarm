import setup_path
import airsim
from drone_controller import DroneController
from astar_algorithm import load_grid_from_csv

def main():
    client = airsim.MultirotorClient()

    # Load map and waypoints for Drone2
    map_data = load_grid_from_csv('map2.csv')
    home = (0, 0)
    waypoints = [(15, 0)]
    target_altitude = -5
    obstacle_threshold = 4

    controller = DroneController(client, "Drone2", home, waypoints, map_data, target_altitude, obstacle_threshold)
    controller.run()

if __name__ == "__main__":
    main()
