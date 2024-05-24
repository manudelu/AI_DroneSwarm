import csv

# Initialize dictionaries to store the values
map1 = {}
map2 = {}
map3 = {}

# Open the CSV file for reading
with open('new_map.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for y, row in enumerate(csvreader):
        # Iterate over each value in the row
        for x, value in enumerate(row):
            # Convert the value to the appropriate data type if needed
            value = int(value)  # Assuming values are integers

            if y <= 21:
                map1[(x, y)] = value
            elif 22 <= y <= 31:
                map2[(x, y - 22)] = value
            else:
                map3[(x, y - 32)] = value

# Write map1 data to a CSV file
with open('output_prova1.csv', 'w', newline='') as csvfile:
    for key, value in map1.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

# Write map2 data to a CSV file
with open('output_prova2.csv', 'w', newline='') as csvfile:
    for key, value in map2.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

# Write map3 data to a CSV file
with open('output_prova3.csv', 'w', newline='') as csvfile:
    for key, value in map3.items():
        csvfile.write(f"({key[0]}, {key[1]}), {value}\n")

print("Output written to CSV files.")
