import json
import airsim
from waypoints import Waypoint

def load_waypoints_from_json(filename):
    waypoints = {}

    # First, create the Waypoint objects without adding neighbors
    with open(filename, 'r') as file:
        data = json.load(file)
        for waypoint_data in data['waypoints']:
            position = waypoint_data['position']
            waypoint = Waypoint(airsim.Vector3r(position['x'], position['y'], position['z']), waypoint_data['name'])
            waypoints[waypoint_data['name']] = waypoint

    # Then, add neighbors to the Waypoint objects
    with open(filename, 'r') as file:
        data = json.load(file)
        for waypoint_data in data['waypoints']:
            for neighbor_data in waypoint_data['neighbors']:
                neighbor_name = neighbor_data['neighbor']
                cost = neighbor_data['cost']
                waypoints[waypoint_data['name']].add_neighbor(waypoints[neighbor_name], cost)

    return list(waypoints.values())  # Convert dictionary values to a list
