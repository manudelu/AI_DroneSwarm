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
