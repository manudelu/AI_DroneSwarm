import csv
from queue import PriorityQueue
import math

def load_grid_from_csv(file_path):
    """
    Load the grid map from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        dict: A dictionary representing the grid map where keys are (x, y) tuples and values are heights.
    """
    grid = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x, y, height = int(row[0].strip('(')), int(row[1].strip(' )')), int(row[2])
            grid[(x, y)] = height
    return grid

def heuristic(a, b):
    """
    Calculate the Manhattan distance heuristic between two points.

    Args:
        a (tuple): The first point (x, y).
        b (tuple): The second point (x, y).

    Returns:
        int: The Manhattan distance between the points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position, grid):
    """
    Get the neighboring positions of a given position in the grid.

    Args:
        position (tuple): The current position (x, y).
        grid (dict): The grid map.

    Returns:
        list: A list of neighboring positions (x, y).
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Include diagonal directions
    neighbors = [(position[0] + dx, position[1] + dy) for dx, dy in directions if (position[0] + dx, position[1] + dy) in grid]
    return neighbors

def astar(grid, start, goal, obstacle_threshold, initial_battery):
    """
    Perform the A* pathfinding algorithm.

    Args:
        grid (dict): The grid map.
        start (tuple): The starting position (x, y).
        goal (tuple): The goal position (x, y).
        obstacle_threshold (int): The height threshold for obstacles.
        initial_battery (float): The initial battery percentage.

    Returns:
        tuple: The path from start to goal and the remaining battery level.
    """
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    battery_level = {start: initial_battery}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            break

        for next_node in get_neighbors(current, grid):
            if grid[next_node] > obstacle_threshold:
                continue  # Skip nodes above the obstacle threshold

            move_cost = math.sqrt(2) if abs(next_node[0] - current[0]) == 1 and abs(next_node[1] - current[1]) == 1 else 1
            height_diff = abs(grid[next_node] - grid[current])
            new_cost = cost_so_far[current] + move_cost + height_diff
            new_battery_level = battery_level[current] - 0.5 * (move_cost + height_diff)

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                battery_level[next_node] = new_battery_level
                priority = new_cost + heuristic(next_node, goal)
                open_set.put((priority, next_node))
                came_from[next_node] = current

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()

    if path[0] != start or battery_level.get(goal, 0) <= 0:
        return None, "Battery depleted before reaching the goal."

    return path, round(battery_level[goal])
