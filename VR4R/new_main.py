import airsim
import sys
import time
import setup_path
from astar_algorithm import astar
from waypoints import Waypoint
from waypoints_loader import load_waypoints_from_json

# Import obstacle avoidance components
from obstacle_avoidance import get_lidar_data, process_lidar_data, avoid_obstacles, apply_force

# Load waypoints from JSON file
waypoints = load_waypoints_from_json('waypoints.json')

# Calculate the path using A* algorithm
start_waypoint = waypoints[0]  # Starting waypoint
goal_waypoint = waypoints[-1]   # Goal waypoint
path = astar(start_waypoint, goal_waypoint)

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print("Connected!")

print("Arming the drone...")
client.armDisarm(True)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("Taking off...")
    client.takeoffAsync().join()
else:
    client.hoverAsync().join()

time.sleep(1)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("Take off failed...")
    sys.exit(1)

# AirSim uses NED coordinates so negative axis is up.
# z of -5 is 5 meters above the original launch point.
z = -5
print("Make sure we are hovering at {} meters...".format(-z))
client.moveToZAsync(z, 1).join()

# Execute the drone movement through waypoints
print("Flying on path...")

for i in range(len(path) - 1):
    current_waypoint = path[i]
    next_waypoint = path[i + 1]
    print(f"Moving towards {next_waypoint.name}")
    client.moveToPositionAsync(next_waypoint.position.x_val, next_waypoint.position.y_val, z, 1).join()
    print(f"Reached {next_waypoint.name}")

    # Integrate obstacle avoidance logic
    lidar_data = get_lidar_data(client)
    obstacles = process_lidar_data(lidar_data)
    avoidance_force = avoid_obstacles(obstacles, client.getMultirotorState().kinematics_estimated.linear_velocity.to_numpy_array(), 0.1)
    apply_force(client, avoidance_force)

# Land the drone
print("Landing...")
client.landAsync().join()
print("Disarming...")
client.armDisarm(False)
client.enableApiControl(False)
print("Done.")
