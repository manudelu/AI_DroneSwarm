import binvox_rw
import numpy as np
import csv

def load_binvox(filename):
    """
    Load a .binvox file and return its voxel data.

    Args:
        filename (str): Path to the .binvox file.

    Returns:
        np.ndarray: 3D numpy array representing the voxel data.
    """
    try:
        with open(filename, 'rb') as f:
            binvox_model = binvox_rw.read_as_3d_array(f)
        return binvox_model.data
    except Exception as e:
        print(f"Error loading binvox file: {e}")
        return None

def extract_2_5D_map(binvox_data):
    """
    Extract a 2.5D map (top-down view) from 3D voxel data by summing along the z-axis.

    Args:
        binvox_data (np.ndarray): 3D numpy array representing the voxel data.

    Returns:
        np.ndarray: 2D numpy array representing the 2.5D map.
    """
    if binvox_data is None:
        return None
    map_2D = np.sum(binvox_data, axis=2)
    return map_2D

def save_to_csv(data, filename):
    """
    Save 2.5D map data to a CSV file.

    Args:
        data (np.ndarray): 2D numpy array representing the 2.5D map.
        filename (str): Path to the output CSV file.
    """
    if data is None:
        print("No data to save.")
        return
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
        print(f"Output written to {filename}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

if __name__ == "__main__":
    binvox_file = "map.binvox"
    binvox_data = load_binvox(binvox_file)
    
    if binvox_data is not None:
        map_2D = extract_2_5D_map(binvox_data)
        csv_file = "map.csv"
        save_to_csv(map_2D, csv_file)
    else:
        print("Failed to process .binvox file.")
