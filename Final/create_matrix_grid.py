class GridGraph:
    def __init__(self, size):
        self.size = size
        self.graph = {(i, j): [] for i in range(size) for j in range(56)}

    def add_edge(self, cell1, cell2):
        if cell1 in self.graph and cell2 in self.graph and cell2 not in self.graph[cell1]:
            self.graph[cell1].append(cell2)
            self.graph[cell2].append(cell1)

    def are_connected(self, cell1, cell2):
        return cell2 in self.graph[cell1]

import csv

# Initialize dictionaries to store the values
map1 = {}
map2 = {}
map3 = {}

grid1 = GridGraph(22)
grid2 = GridGraph(10)
grid3 = GridGraph(24)

# Function to add edges for all neighbors including diagonal
def add_all_neighbors(grid, i, j, max_i, max_j):
    # Define all possible neighbor directions (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < max_i and 0 <= nj < max_j:
            grid.add_edge((i, j), (ni, nj))

# Open the CSV file for reading
with open('map.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for i, row in enumerate(csvreader):
        # Iterate over each value in the row
        for j, value in enumerate(row):
            # Convert the value to the appropriate data type if needed
            value = int(value)  # Assuming values are integers

            if i <= 21:
                map1[(i, j)] = value
                add_all_neighbors(grid1, i, j, 22, len(row))
            elif 22 <= i <= 31:
                map2[(i - 22, j)] = value
                add_all_neighbors(grid2, i - 22, j, 10, len(row))
            else:
                map3[(i - 32, j)] = value
                add_all_neighbors(grid3, i - 32, j, 24, len(row))

with open('porcodio.txt', 'w') as txtfile:
    # Write map1 data
    txtfile.write("Map1:\n")
    for key, value in map1.items():
        txtfile.write(f"{key}: {value}\n")

    txtfile.write("\nMap1 Neighbors:\n")
    for cell, neighbors in grid1.graph.items():
        neighbor_str = ', '.join([f"({x}, {y})" for x, y in neighbors])
        txtfile.write(f"Cell {cell}: Neighbors -> {neighbor_str}\n")

    txtfile.write("\n")

    # Write map2 data
    txtfile.write("\nMap2:\n")
    for key, value in map2.items():
        txtfile.write(f"{key}: {value}\n")

    txtfile.write("\nMap2 Neighbors:\n")
    for cell, neighbors in grid2.graph.items():
        neighbor_str = ', '.join([f"({x}, {y})" for x, y in neighbors])
        txtfile.write(f"Cell {cell}: Neighbors -> {neighbor_str}\n")

    txtfile.write("\n")

    # Write map3 data
    txtfile.write("\nMap3:\n")
    for key, value in map3.items():
        txtfile.write(f"{key}: {value}\n")

    txtfile.write("\nMap3 Neighbors:\n")
    for cell, neighbors in grid3.graph.items():
        neighbor_str = ', '.join([f"({x}, {y})" for x, y in neighbors])
        txtfile.write(f"Cell {cell}: Neighbors -> {neighbor_str}\n")

print("Output written to output.txt file.")
