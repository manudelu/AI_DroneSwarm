import airsim
import os

def create_voxel_map():
    c = airsim.VehicleClient()
    center = airsim.Vector3r(28, 28, 0)
    output_path = os.path.join(os.getcwd(), "map.binvox")
    c.simCreateVoxelGrid(center, 56, 56, 56, 1, output_path)
    print(f"Voxel map created to {output_path}")

if __name__ == "__main__":
    create_voxel_map()


# In order to visualize the .binvox install viewvox from this link: https://www.patrickmin.com/viewvox/
