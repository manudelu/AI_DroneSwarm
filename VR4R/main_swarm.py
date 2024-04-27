import airsim
import pprint
import setup_path 
import sys
import time
import math  
from astar_algorithm import astar
from waypoints import Waypoint
from waypoints_loader import load_waypoints_from_json

# Load waypoints from JSON file
waypoints = load_waypoints_from_json('waypoints.json')

# Calculate the path using A* algorithm
start_waypoint = waypoints[0]  # Starting waypoint
goal_waypoint = waypoints[6]   # Goal waypoint
path = astar(start_waypoint, goal_waypoint)

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
# z of -5 is 5 meters above the original launch point.
z = -5
print("Make sure we are hovering at {} meters...".format(-z))
f1 = client.moveToZAsync(z, 1, vehicle_name="Drone1")
f2 = client.moveToZAsync(z, 1, vehicle_name="Drone2")
f1.join()
f2.join()

# Loop through waypoints and navigate while rotating to face each waypoint
for i in range(len(path) - 1):
    current_waypoint = path[i]
    next_waypoint = path[i + 1]

    # Calculate the yaw angle to face the next waypoint
    dx = next_waypoint.position.x_val - current_waypoint.position.x_val
    dy = next_waypoint.position.y_val - current_waypoint.position.y_val
    yaw = math.degrees(math.atan2(dy, dx))

    # Rotate the drone to face the next waypoint
    f1 = client.rotateToYawAsync(yaw, vehicle_name="Drone1")
    f1.join()

    # Move towards the next waypoint
    print(f"Moving towards {next_waypoint.name}")
    f1 = client.moveToPositionAsync(next_waypoint.position.x_val, next_waypoint.position.y_val, next_waypoint.position.z_val, 1)
    f1.join()
    print(f"Reached {next_waypoint.name}")

# Land the drone
print("Landing...")
f1 = client.landAsync(vehicle_name="Drone1")
f2 = client.landAsync(vehicle_name="Drone2")
f1.join()
f2.join()

print("Disarming...")
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")

client.enableApiControl(False)
print("Done.")