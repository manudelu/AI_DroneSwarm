import airsim
import sys
import time
import math
import numpy as np
from astar_algorithm import astar
from waypoints import Waypoint
from waypoints_loader import load_waypoints_from_json

# Load waypoints from JSON file
waypoints = load_waypoints_from_json('waypoints.json')

# Calculate the path using A* algorithm
start_waypoint = waypoints[0]  # Starting waypoint
goal_waypoint = waypoints[-1]   # Goal waypoint
path = astar(start_waypoint, goal_waypoint)

class LidarTest:

    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        print("arming the drone...")
        self.client.armDisarm(True)

        airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()

        for waypoint in path:
            current_waypoint = waypoint
            print(f"Moving towards {current_waypoint.name}")

            # Move towards the current waypoint
            self.client.moveToPositionAsync(current_waypoint.position.x_val, 
                                             current_waypoint.position.y_val, 
                                             current_waypoint.position.z_val, 1).join()

            # Continuously monitor for obstacles and adjust drone's trajectory
            while True:
                lidar_data = self.client.getLidarData()

                # Process Lidar data and detect obstacles
                if len(lidar_data.point_cloud) >= 3:
                    points = self.parse_lidar_data(lidar_data)
                    obstacles = self.segment_obstacles(points)

                    if obstacles:
                        print("Detected obstacles:")
                        for obstacle in obstacles[:5]:  # Print first 5 obstacles for debugging
                            print("\t", obstacle)

                        # Obstacle avoidance
                        avoidance_direction = self.calculate_avoidance_direction(obstacles)
                        print("Avoidance direction:", avoidance_direction)
                        self.adjust_trajectory(avoidance_direction)
                    else:
                        print("No obstacles detected. Continuing towards the waypoint.")
                        break

                time.sleep(0.1)  

        print("Reached the goal waypoint. Landing...")
        self.client.landAsync().join()

    def calculate_avoidance_direction(self, obstacles):  # roba da Chat
        centroid = np.mean(obstacles, axis=0)
        avoidance_direction = np.array([centroid[0], centroid[1], 0])  # Avoidance direction in XY plane
        return avoidance_direction

    def adjust_trajectory(self, avoidance_direction):
        print("Adjusting trajectory to avoid obstacles...")
        self.client.moveByVelocityAsync(1, 0, 0, 1).join() 

    def parse_lidar_data(self, data):
        # reshape array of floats to array of [X,Y,Z]
        points = np.array(data.point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/3), 3))
        return points

    def segment_obstacles(self, points):
        # Classify points above a certain height as obstacles
        obstacles = [point for point in points if point[0] < 5]  
        return obstacles

    def stop(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
        print("Done!\n")

if __name__ == "__main__":
    lidarTest = LidarTest()
    try:
        lidarTest.execute()
    finally:
        lidarTest.stop()
