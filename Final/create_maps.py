import csv

# Initialize dictionaries to store the values
map1 = {}
map2 = {}
map3 = {}

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

            if j <= 21:
                map1[(i, j)] = value
            elif 22 <= j <= 31:
                map2[(i, j - 22)] = value
            else:
                map3[(i, j - 32)] = value

# Write map1 data to output_prova1.csv
with open('output_prova1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for (x, y), value in map1.items():
        writer.writerow([f"({x}, {y})", value])

# Write map2 data to output_prova2.csv
with open('output_prova2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for (x, y), value in map2.items():
        writer.writerow([f"({x}, {y})", value])

# Write map3 data to output_prova3.csv
with open('output_prova3.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for (x, y), value in map3.items():
        writer.writerow([f"({x}, {y})", value])

print("Output written to output.txt file.")
