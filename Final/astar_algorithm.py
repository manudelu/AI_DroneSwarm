import csv
from queue import PriorityQueue
import math

# Load the grid from a CSV file
def load_grid_from_csv(file_path):
    grid = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x, y, height = row[0], row[1], row[2]
            # Parse the cell coordinates and height value
            x = int(x.strip('('))
            y = int(y.strip(' )'))
            grid[(x, y)] = int(height)
    return grid

# Define the heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Define a function to get the neighbors of a cell
def get_neighbors(position, grid):
    neighbors = []
    # Include diagonal directions
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                  (1, 1), (1, -1), (-1, 1), (-1, -1)] # Down, Up, Right, Left, and 4 Diagonals
    for direction in directions:
        neighbor = (position[0] + direction[0], position[1] + direction[1])
        if neighbor in grid:  # Check if the neighbor is within grid bounds
            neighbors.append(neighbor)
    return neighbors

# Define the A* pathfinding function
def astar(grid, start, goal, obstacle_threshold):
    # Initialize priority queue for frontier nodes
    open_set = PriorityQueue()
    # Put the starting node into the priority queue with priority 0
    open_set.put((0, start))
    # Initialize dictionaries to track the previous node and cost so far for each node
    came_from = {}
    cost_so_far = {}
    # Set the starting node's previous node to None and its cost so far to 0
    came_from[start] = None
    cost_so_far[start] = 0

    # The algorithm will run until the open set is empty
    while not open_set.empty():
        # Get the current node from the open set with the lowest priority
        _, current = open_set.get()
        # Check if the current node is the goal node, if so, exit the loop
        if current == goal:
            break

        # Explore neighbors of the current node
        for next_node in get_neighbors(current, grid):
            # Check if the terrain height exceeds the obstacle threshold
            if grid[next_node] > obstacle_threshold:
                continue # Skip this node if it's above the obstacle threshold
            # Calculate the movement cost
            if abs(next_node[0] - current[0]) == 1 and abs(next_node[1] - current[1]) == 1:
                move_cost = math.sqrt(2)  # Diagonal movement cost
            else:
                move_cost = 1  # Non-diagonal movement cost
            
            height_diff = abs(grid[next_node] - grid[current])
            new_cost = cost_so_far[current] + move_cost + height_diff

            # If the neighbor has not been visited yet or the new cost is lower than previous cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                # Update the cost so far for the neighbor
                cost_so_far[next_node] = new_cost
                # Calculate the priority of the neighbor based on its cost and heuristic
                priority = new_cost + heuristic(next_node, goal)
                # Put the neighbor into the open set with its priority
                open_set.put((priority, next_node))
                # Update the previous node for the neighbor
                came_from[next_node] = current

    # Reconstruct the path from start to goal
    path = []
    current = goal
    while current is not None:
        # Add the current node to the path
        path.append(current)
        # Move to the previous node
        current = came_from[current]
    # Reverse the path to get it from start to goal
    path.reverse()
    return path