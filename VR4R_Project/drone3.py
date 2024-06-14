import setup_path
import airsim
from drone_controller import DroneController
from astar_algorithm import load_grid_from_csv
import config  

def main():
    client = airsim.MultirotorClient()

    # Load map and waypoints for Drone3
    map_data = load_grid_from_csv('map3.csv')
    waypoints = [(20, 40), (35, 45)]

    # Get initial pose of the drone
    initial_pose = client.simGetObjectPose("Drone3")
    x_start = initial_pose.position.x_val
    y_start = initial_pose.position.y_val
    waypoints = [(x - x_start, y - y_start) for x, y in waypoints]

    controller = DroneController(client, "Drone3", config.home, waypoints, map_data, config.target_altitude, config.obstacle_threshold)
    controller.run()

if __name__ == "__main__":
    main()
