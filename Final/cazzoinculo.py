import csv

# Initialize dictionaries to store the values
map1 = {}
map2 = {}
map3 = {}

def calculate_cost(grid, i, j):
    # Define the relative positions of all 24 possible neighbors within a distance of 2
    neighbors = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                 (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                 (0, -2),  (0, -1),           (0, 1),  (0, 2),
                 (1, -2),  (1, -1),  (1, 0),  (1, 1),  (1, 2),
                 (2, -2),  (2, -1),  (2, 0),  (2, 1),  (2, 2)]
    total = float(grid[i][j])
    count = 1

    for di, dj in neighbors:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            total += float(grid[ni][nj])
            count += 1

    return (total / count)**2  # Float division for average, highlighted by exponential

# Read the entire CSV file into a 2D list
grid = []
with open('new_map.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        grid.append([int(value) for value in row])

# Iterate over each cell in the grid
for i in range(len(grid)):
    for j in range(len(grid[i])):
        value = grid[i][j]

        if value < 5:
            cost = calculate_cost(grid, i, j)
        else:
            cost = value**2

        if j <= 21:
            map1[(i, j)] = (value, cost)
        elif 22 <= j <= 31:
            map2[(i, j - 22)] = (value, cost)
        else:
            map3[(i, j - 32)] = (value, cost)

# Write the dictionaries to text files
with open('output_prova1.txt', 'w') as txtfile:
    # Write map1 data
    for key, value in map1.items():
        txtfile.write(f"{key}, {value}\n")

with open('output_prova2.txt', 'w') as txtfile:
    # Write map2 data
    for key, value in map2.items():
        txtfile.write(f"{key}, {value}\n")

with open('output_prova3.txt', 'w') as txtfile:
    # Write map3 data
    for key, value in map3.items():
        txtfile.write(f"{key}, {value}\n")

print("Output written to output files.")
