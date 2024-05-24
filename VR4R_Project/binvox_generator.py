import airsim
import os

def binvox_generator():
    c = airsim.VehicleClient()
    center = airsim.Vector3r(0, 0, 0)
    output_path = os.path.join(os.getcwd(), "map.binvox")
    c.simCreateVoxelGrid(center, 56, 56, 56, 1, output_path)

# In order to visualize the .binvox install viewvox from this link: https://www.patrickmin.com/viewvox/