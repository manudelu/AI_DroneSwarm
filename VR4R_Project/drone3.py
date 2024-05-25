import setup_path
import airsim
from astar_algorithm import load_grid_from_csv, astar

def main():
    # Load the grid map for Drone 3
    map3 = load_grid_from_csv('map3.csv')

    # Define altitude control parameters
    target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
    obstacle_threshold = 4  # Obstacle height threshold

    # Define the home and goal positions for Drone 3
    home = (0, 0)
    goal3 = (10, 0)

    # Run the A* algorithm and print the path
    path3 = astar(map3, home, goal3, obstacle_threshold)

    # Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
    airsim_path3 = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in path3]

    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Drone3 connected!")

    client.enableApiControl(True, "Drone3")
    print("Drone3 arming...")
    client.armDisarm(True, "Drone3")

    client.takeoffAsync(vehicle_name="Drone3").join()

    print(f"Drone3 hovering at {abs(target_altitude)} meters...")
    client.moveToZAsync(target_altitude, 3, vehicle_name="Drone3").join()

    # Use moveOnPathAsync to follow the path
    print("Drone3 following the path...")
    client.moveOnPathAsync(airsim_path3, velocity=1, vehicle_name="Drone3", 
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone3 path followed successfully.")

    # Return home
    print("Drone3 returning home...")
    return_path3 = astar(map3, goal3, home, obstacle_threshold)
    return_airsim_path3 = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in return_path3]

    client.moveOnPathAsync(return_airsim_path3, velocity=1, vehicle_name="Drone3", 
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone3 returned home successfully.")

    # Land the drone
    print("Drone3 landing...")
    client.landAsync(vehicle_name="Drone3").join()

    print("Drone3 disarming...")
    client.armDisarm(False, "Drone3")
    client.enableApiControl(False, "Drone3")
    print("Drone3 done.")

if __name__ == "__main__":
    main()
