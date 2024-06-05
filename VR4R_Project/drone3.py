import setup_path
import airsim
from drone_controller import DroneController
from astar_algorithm import load_grid_from_csv
import config  

def main():
    client = airsim.MultirotorClient()

    # Load map and waypoints for Drone3
    map_data = load_grid_from_csv('map3.csv')
    waypoints = [(10, 0)]

    controller = DroneController(client, "Drone3", config.home, waypoints, map_data, config.target_altitude, config.obstacle_threshold)
    controller.run()

if __name__ == "__main__":
    main()
