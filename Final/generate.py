import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

# Import functions from the maps folder
from maps.create_map import create_map
from maps.separate_map import separate_map
from maps.binvox_generator import binvox_generator

# Set the path to the maps folder
maps_folder = "maps"

# Generate binvox model
binvox_generator()

# Create map
create_map()

# Separate map
separate_map()

print("Process completed.")
