import setup_path
import airsim
from astar_algorithm import load_grid_from_csv, astar
import time

def main():
    # Load the grid map for Drone 2
    map2 = load_grid_from_csv('map2.csv')

    # Define altitude control parameters
    target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
    obstacle_threshold = 4  # Obstacle height threshold
    initial_battery = 100.00  # Initial battery percentage

    # Define the home and goal positions for Drone 2
    home = (0, 0)
    goal2 = (15, 0)

    # Run the A* algorithm and print the path
    path2, status = astar(map2, home, goal2, obstacle_threshold, initial_battery)
    # Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
    airsim_path2 = [airsim.Vector3r(x, y, target_altitude - map2[(x, y)] + 1) for x, y in path2]

    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Drone2 connected!")

    client.enableApiControl(True, "Drone2")
    print("Drone2 arming...")
    client.armDisarm(True, "Drone2")

    time.sleep(1)
    client.takeoffAsync(vehicle_name="Drone2").join()
    time.sleep(1)
    print(f"Drone2 hovering at {abs(target_altitude)} meters...")
    client.moveToZAsync(target_altitude, 1, vehicle_name="Drone2").join()
    time.sleep(1)

    # Use moveOnPathAsync to follow the path
    print("Drone2 following the path...")
    print(path2)
    client.moveOnPathAsync(airsim_path2, velocity=2, vehicle_name="Drone2", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone2 path followed successfully.")
    print(f"Remaining battery: {status} %")

    time.sleep(1)

    # Return home
    print("Drone2 returning home...")
    return_path2, status = astar(map2, goal2, home, obstacle_threshold, status)
    return_airsim_path2 = [airsim.Vector3r(x, y, target_altitude - map2[(x, y)] + 1) for x, y in return_path2]
    print(return_path2)

    client.moveOnPathAsync(return_airsim_path2, velocity=2, vehicle_name="Drone2", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone2 returned home successfully.")
    print(f"Remaining battery: {status} %")

    # Land the drone
    time.sleep(1)
    client.moveToZAsync(-3, 1, vehicle_name="Drone2").join()
    time.sleep(1)
    print("Drone2 landing...")
    client.landAsync(vehicle_name="Drone2").join()

    print("Drone2 disarming...")
    client.armDisarm(False, "Drone2")
    client.enableApiControl(False, "Drone2")
    print("Drone2 done.")

if __name__ == "__main__":
    main()
