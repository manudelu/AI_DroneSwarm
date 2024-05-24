import setup_path
import airsim
import pprint
import sys
import time
from astar_algorithm import load_grid_from_csv, astar

# Load the grid
grid = load_grid_from_csv('output_prova1.csv')

# Define the start and goal positions
start = (0, 0)
goal = (55, 21)

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
client.enableApiControl(True, "Drone2")

print("Arming the drones...")
client.armDisarm(True, "Drone1")
client.armDisarm(True, "Drone2")

f1 = client.takeoffAsync(vehicle_name="Drone1")
f2 = client.takeoffAsync(vehicle_name="Drone2")
f1.join()
f2.join()

state1 = client.getMultirotorState(vehicle_name="Drone1")
s = pprint.pformat(state1)
print("state: %s" % s)
state2 = client.getMultirotorState(vehicle_name="Drone2")
s = pprint.pformat(state2)
print("state: %s" % s)

# AirSim uses NED coordinates so negative axis is up.
print("Make sure we are hovering at {} meters...".format(-target_altitude))
f1 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone1")
f2 = client.moveToZAsync(target_altitude, 3, vehicle_name="Drone2")
f1.join()
f2.join()

# Convert the path to a list of AirSim Vector3r objects with the correct Z coordinate
airsim_path = [airsim.Vector3r(x, y, target_altitude - grid[(x, y)] + 1) for x, y in path]
# Print waypoints for debugging
print("Waypoints with altitude adjustment:")
for waypoint in airsim_path:
    print("Waypoint:", waypoint)

# Use moveOnPathAsync to follow the path
print("Following the path...")
f1 = client.moveOnPathAsync(airsim_path, velocity=2, vehicle_name="Drone1", 
                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0), 
                            lookahead=-1, adaptive_lookahead=1)
f1.join()
print("Path followed successfully.")

# Land the drone
print("Landing...")
f1 = client.landAsync(vehicle_name="Drone1")
f2 = client.landAsync(vehicle_name="Drone2")
f1.join()
f2.join()

print("Disarming...")
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")

client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
print("Done.")