import setup_path
import airsim
from drone_controller import DroneController
from astar_algorithm import load_grid_from_csv
import config  

def main():
    client = airsim.MultirotorClient()

    # Load map and waypoints for Drone2
    map_data = load_grid_from_csv('map2.csv')
    waypoints = [(15, 21), (30, 30)]

    # Get initial pose of the drone
    initial_pose = client.simGetObjectPose("Drone2")
    x_start = initial_pose.position.x_val
    y_start = initial_pose.position.y_val
    waypoints = [(x - x_start, y - y_start) for x, y in waypoints]

    controller = DroneController(client, "Drone2", config.home, waypoints, map_data, config.target_altitude, config.obstacle_threshold)
    controller.run()

if __name__ == "__main__":
    main()
