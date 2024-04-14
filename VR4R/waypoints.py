# Define a class for representing waypoints in the graph 
class Waypoint:
    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor, cost):
        self.neighbors.append((neighbor, cost))

    def cost(self, next_node):
        for neighbor, cost in self.neighbors:
            if neighbor == next_node:
                return cost
        return float('inf')  # Return infinity if the neighbor is not found
    
    # Define comparison methods for nodes
    def __lt__(self, other):
        return False  # No meaningful comparison, always return False
    
    def __eq__(self, other):
        return False  # No meaningful comparison, always return False
    
    # Define hash method for nodes
    def __hash__(self):
        return hash(self.position)
