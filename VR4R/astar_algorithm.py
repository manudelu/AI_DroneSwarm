# Import necessary libraries
from queue import PriorityQueue

# Define a function for A* pathfinding
def astar(start, goal):
    # Initialize priority queue for frontier nodes
    open_set = PriorityQueue()
    # Put the starting node into the priority queue with priority 0
    open_set.put(start, 0)
    # Initialize dictionaries to track the previous node and cost so far for each node (gScore[n])
    came_from = {}
    cost_so_far = {}
    # Set the starting node's previous node to None and its cost so far to 0
    came_from[start] = None
    cost_so_far[start] = 0

    # The algorithm will run until the open set is empty
    while not open_set.empty():
        # Get the current node from the open set with the lowest priority
        current = open_set.get()
        # Check if the current node is the goal node, if so, exit the loop
        if current == goal:
            break

        # Explore neighbors of the current node
        for next_node, _ in current.neighbors:
            # Calculate the cost to reach the neighbor from the current node
            new_cost = cost_so_far[current] + current.cost(next_node)
            # If the neighbor has not been visited yet or the new cost is lower than previous cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                # Update the cost so far for the neighbor
                cost_so_far[next_node] = new_cost
                # Define a heuristic variable (h[n]) for A* (Euclidean distance)
                heuristic = abs(next_node.position.x_val - goal.position.x_val) + abs(next_node.position.y_val - goal.position.y_val)
                # Calculate the priority (fScore[n]) of the neighbor based on its cost and heuristic
                priority = new_cost + heuristic
                # Put the neighbor into the open set with its priority
                open_set.put(next_node, priority)
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