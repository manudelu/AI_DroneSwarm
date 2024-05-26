import setup_path
import airsim
from astar_algorithm import load_grid_from_csv, astar
import time

def main():
    # Load the grid map for Drone 1
    map1 = load_grid_from_csv('map1.csv')

    # Define altitude control parameters
    target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
    obstacle_threshold = 4  # Obstacle height threshold
    initial_battery = 100.00  # Initial battery percentage

    # Define the home and goal positions for Drone 1
    home = (0, 0)
    goal1 = (44, -15)

    # Run the A* algorithm and print the path
    path1, status = astar(map1, home, goal1, obstacle_threshold, initial_battery)
    # Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
    airsim_path1 = [airsim.Vector3r(x, y, target_altitude - map1[(x, y)] + 1) for x, y in path1]

    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Drone1 connected!")

    client.enableApiControl(True, "Drone1")
    print("Drone1 arming...")
    client.armDisarm(True, "Drone1")

    # Take off
    time.sleep(1)
    client.takeoffAsync(vehicle_name="Drone1").join()
    time.sleep(1)
    print(f"Drone1 hovering at {abs(target_altitude)} meters...")
    client.moveToZAsync(target_altitude, 1, vehicle_name="Drone1").join()
    time.sleep(1)

    # Use moveOnPathAsync to follow the path
    print("Drone1 following the path...")
    print(path1)
    client.moveOnPathAsync(airsim_path1, velocity=2, vehicle_name="Drone1", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone1 path followed successfully.")
    print(f"Remaining battery: {status} %")
    
    time.sleep(1)
    
    # Return home
    print("Drone1 returning home...")
    return_path1, status = astar(map1, goal1, home, obstacle_threshold, status)
    return_airsim_path1 = [airsim.Vector3r(x, y, target_altitude - map1[(x, y)] + 1) for x, y in return_path1]
    print(return_path1)

    client.moveOnPathAsync(return_airsim_path1, velocity=2, vehicle_name="Drone1", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1).join()
    print("Drone1 returned home successfully.")
    print(f"Remaining battery: {status} %")

    # Land the drone
    time.sleep(1)
    client.moveToZAsync(-3, 1, vehicle_name="Drone1").join()
    time.sleep(1)
    print("Drone1 landing...")
    client.landAsync(vehicle_name="Drone1").join()

    print("Drone1 disarming...")
    client.armDisarm(False, "Drone1")
    client.enableApiControl(False, "Drone1")
    print("Drone1 done.")

if __name__ == "__main__":
    main()
