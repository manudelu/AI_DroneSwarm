import setup_path
import airsim
from astar_algorithm import load_grid_from_csv, astar

# Load the grid maps
map1 = load_grid_from_csv('map1.csv')
map2 = load_grid_from_csv('map2.csv')
map3 = load_grid_from_csv('map3.csv')

# Define altitude control parameters
target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
obstacle_threshold = 4  # Obstacle height threshold

# Define the home position for each drone
home = (0, 0)

# Define the goal positions for each drone
goal1 = (10, 0)
goal2 = (10, 0)
goal3 = (10, 0)

# Run the A* algorithm and print the path
path1 = astar(map1, home, goal1, obstacle_threshold)
path2 = astar(map2, home, goal2, obstacle_threshold)
path3 = astar(map3, home, goal3, obstacle_threshold)

# Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
airsim_path1 = [airsim.Vector3r(x, y, target_altitude - map1[(x, y)] + 1) for x, y in path1]
airsim_path2 = [airsim.Vector3r(x, y, target_altitude - map2[(x, y)] + 1) for x, y in path2]
airsim_path3 = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in path3]

client = airsim.MultirotorClient()
client.confirmConnection()
print("Connected!")

client.enableApiControl(True, "Drone1")
client.enableApiControl(True, "Drone2")
client.enableApiControl(True, "Drone3")

print("Arming the drones...")
client.armDisarm(True, "Drone1")
client.armDisarm(True, "Drone2")
client.armDisarm(True, "Drone3")

f1 = client.takeoffAsync(vehicle_name="Drone1")
f2 = client.takeoffAsync(vehicle_name="Drone2")
f3 = client.takeoffAsync(vehicle_name="Drone3")
f1.join()
f2.join()
f3.join()

# AirSim uses NED coordinates so negative axis is up.
print("Make sure we are hovering at {} meters...".format(-target_altitude))
f1 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone1")
f2 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone2")
f2 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone3")
f1.join()
f2.join()
f3.join()

# Use moveOnPathAsync to follow the path
print("Following the path...")
f1 = client.moveOnPathAsync(airsim_path1, velocity=1, vehicle_name="Drone1", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f2 = client.moveOnPathAsync(airsim_path2, velocity=1, vehicle_name="Drone2", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f3 = client.moveOnPathAsync(airsim_path3, velocity=1, vehicle_name="Drone3", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f1.join()
f2.join()
f3.join()
print("Path followed successfully.")

# Return home
print("Returning home...")
return_path1 = astar(map1, goal1, home, obstacle_threshold)
return_path2 = astar(map2, goal2, home, obstacle_threshold)
return_path3 = astar(map3, goal3, home, obstacle_threshold)
return_airsim_path1 = [airsim.Vector3r(x, y, target_altitude - map1[(x, y)] + 1) for x, y in return_path1]
return_airsim_path2 = [airsim.Vector3r(x, y, target_altitude - map2[(x, y)] + 1) for x, y in return_path2]
return_airsim_path3 = [airsim.Vector3r(x, y, target_altitude - map3[(x, y)] + 1) for x, y in return_path3]

# Use moveOnPathAsync to return to the home position
f1 = client.moveOnPathAsync(return_airsim_path1, velocity=1, vehicle_name="Drone1", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f2 = client.moveOnPathAsync(return_airsim_path2, velocity=1, vehicle_name="Drone2", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f3 = client.moveOnPathAsync(return_airsim_path3, velocity=1, vehicle_name="Drone3", drivetrain = airsim.DrivetrainType.ForwardOnly,
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f1.join()
f2.join()
f3.join()
print("Returned home successfully.")

# Land the drone
print("Landing...")
f1 = client.landAsync(vehicle_name="Drone1")
f2 = client.landAsync(vehicle_name="Drone2")
f3 = client.landAsync(vehicle_name="Drone3")
f1.join()
f2.join()
f3.join()

print("Disarming...")
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")
client.armDisarm(False, "Drone3")

client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
client.enableApiControl(False, "Drone3")
print("Done.")