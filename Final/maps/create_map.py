import binvox_rw
import numpy as np
import csv

def create_map():
    # Load .binvox file
    def load_binvox(filename):
        with open(filename, 'rb') as f:
            binvox_model = binvox_rw.read_as_3d_array(f)
        return binvox_model.data

    # Extract 2.5D map data (top-down view)
    def extract_2_5D_map(binvox_data):
        # Sum along the z-axis to get 2D representation
        map_2D = np.sum(binvox_data, axis=2)
        return map_2D

    # Save 2.5D map data to CSV file
    def save_to_csv(data, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

    # Example usage
    if __name__ == "__main__":
        # Load .binvox file
        binvox_file = "map.binvox"
        binvox_data = load_binvox(binvox_file)
        
        # Extract 2.5D map data
        map_2D = extract_2_5D_map(binvox_data)
        
        # Save to CSV file
        csv_file = "map.csv"
        save_to_csv(map_2D, csv_file)
