import setup_path
import airsim
import pprint
import sys
import time
from astar_algorithm import load_grid_from_csv, astar

# Load the grid
grid = load_grid_from_csv('map1.csv')

# Define the start and goal positions
start = (0, 0)
goal = (48, 21)

# Define the home position
home = (0, 0) 

# Define altitude control parameters
target_altitude = -5  # Target altitude (NED coordinates, so negative is up)
obstacle_threshold = 4  # Obstacle height threshold

# Run the A* algorithm and print the path
path = astar(grid, start, goal, obstacle_threshold)
print("Path:", path)

client = airsim.MultirotorClient()
client.confirmConnection()
print("Connected!")

client.enableApiControl(True, "Drone1")

print("Arming the drone...")
client.armDisarm(True, "Drone1")

f1 = client.takeoffAsync(vehicle_name="Drone1")
f1.join()

state = client.getMultirotorState(vehicle_name="Drone1")
s = pprint.pformat(state1)
print("state: %s" % s)

# AirSim uses NED coordinates so negative axis is up.
print("Make sure we are hovering at {} meters...".format(-target_altitude))
f1 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone1")
f1.join()

# Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
airsim_path = [airsim.Vector3r(x, y, target_altitude - grid[(x, y)] + 1) for x, y in path]

# Print waypoints for debugging
print("Waypoints with altitude adjustment:")
for waypoint in airsim_path:
    print("Waypoint:", waypoint)

# Use moveOnPathAsync to follow the path
print("Following the path...")
f1 = client.moveOnPathAsync(airsim_path, velocity=3, vehicle_name="Drone1", 
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f1.join()
print("Path followed successfully.")

# Return home
print("Returning home...")
return_path = astar(grid, goal, home, obstacle_threshold)
return_airsim_path = [airsim.Vector3r(x, y, target_altitude - grid[(x, y)] + 1) for x, y in return_path]

# Print waypoints for debugging
print("Waypoints for return journey:")
for waypoint in return_airsim_path:
    print("Waypoint:", waypoint)

# Use moveOnPathAsync to return to the home position
f1 = client.moveOnPathAsync(return_airsim_path, velocity=3, vehicle_name="Drone1", 
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f1.join()
print("Returned home successfully.")

# Land the drone
print("Landing...")
f1 = client.landAsync(vehicle_name="Drone1")
f1.join()

print("Disarming...")
client.armDisarm(False, "Drone1")

client.enableApiControl(False, "Drone1")
print("Done.")
