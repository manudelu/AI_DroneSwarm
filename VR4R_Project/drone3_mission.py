import setup_path
import airsim
from astar_algorithm import load_grid_from_csv, astar
import time

# Function to return home if the battery is below a threshold
def return_home_if_low_battery(client, current_position, home, map_data, target_altitude, obstacle_threshold, status):
    if status < 30:
        print("Battery low! Returning home...")
        path, status = astar(map_data, current_position, home, obstacle_threshold, status)
        if path:
            return_path = [airsim.Vector3r(x, y, target_altitude - map_data[(x, y)] + 1) for x, y in path]
            client.moveOnPathAsync(return_path, velocity=3, vehicle_name="Drone1", drivetrain=airsim.DrivetrainType.ForwardOnly,
                                   yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                                   lookahead=-1, adaptive_lookahead=1).join()
            print("Drone1 returned home successfully.")
            print(f"Remaining battery: {round(status)}%")
        else:
            print("Failed to return home due to critically low battery. Emergency landing...")
        return True
    return False


def main():
    # Load the grid map for Drone 3
    map3 = load_grid_from_csv('map3.csv')

    # Define altitude control parameters
    target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
    obstacle_threshold = 4  # Obstacle height threshold
    initial_battery = 100.00  # Initial battery percentage

    # Define the home and goal positions for Drone 3
    home = (0, 0)
    waypoints = [(10, 0)]
    current_position = home

    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Drone3 connected!")

    client.enableApiControl(True, "Drone3")
    print("Drone3 arming...")
    client.armDisarm(True, "Drone3")

    time.sleep(1)

    client.takeoffAsync(vehicle_name="Drone3").join()

    time.sleep(1)

    print(f"Drone3 hovering at {abs(target_altitude)} meters...")
    client.moveToZAsync(target_altitude, 1, vehicle_name="Drone3").join()

    time.sleep(1)

    # Visit each waypoint
    for waypoint in waypoints:
        print(f"Drone3 moving to waypoint {waypoint}...")
        path, status = astar(map3, current_position, waypoint, obstacle_threshold, initial_battery)
        airsim_path = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in path]
        client.moveOnPathAsync(airsim_path, velocity=3, vehicle_name="Drone3", drivetrain=airsim.DrivetrainType.ForwardOnly,
                               yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                               lookahead=-1, adaptive_lookahead=1).join()
        print(f"Drone3 reached waypoint {waypoint}.")
        print(f"Remaining battery: {round(status)}%")
        
        # Check battery level and return home if necessary
        if return_home_if_low_battery(client, waypoint, home, map3, target_altitude, obstacle_threshold, status):
            break
        
        current_position = waypoint
        initial_battery = status  # Update the battery level for the next segment

    # If the drone did not return home due to low battery, return home at the end of the mission
    if status >= 30:
        print("Drone3 returning home after completing the mission...")
        return_path, status = astar(map3, current_position, home, obstacle_threshold, status)
        return_airsim_path = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in return_path]
        client.moveOnPathAsync(return_airsim_path, velocity=3, vehicle_name="Drone3", drivetrain=airsim.DrivetrainType.ForwardOnly,
                               yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                               lookahead=-1, adaptive_lookahead=1).join()
        print("Drone3 returned home successfully.")
        print(f"Remaining battery: {round(status)}%")

    time.sleep(1)

    client.moveToZAsync(-3, 1, vehicle_name="Drone3").join()

    time.sleep(1)

    # Land the drone
    print("Drone3 landing...")
    client.landAsync(vehicle_name="Drone3").join()

    print("Drone3 disarming...")
    client.armDisarm(False, "Drone3")

    client.enableApiControl(False, "Drone3")
    print("Drone3 done.")

if __name__ == "__main__":
    main()
