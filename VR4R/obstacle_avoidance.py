import airsim
import time
import numpy as np

threshold_distance = 2.0
max_force = 10.0
kp = 1.0
kd = 0.1
ki = 0.01

class PIDController:
    def __init__(self, kp, kd, ki):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.last_error = 0
        self.integral = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        output = self.kp * error + self.kd * derivative + self.ki * self.integral
        self.last_error = error
        return output

def get_lidar_data(client):
    return client.getLidarData()

def process_lidar_data(lidar_data):
    obstacles = []
    if len(lidar_data.point_cloud) > 3:
        points = np.array(lidar_data.point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/3), 3))
        distances = np.linalg.norm(points, axis=1)
        valid_points_indices = np.where(distances < threshold_distance)[0]
        obstacles = points[valid_points_indices]
    return obstacles

def avoid_obstacles(obstacles, current_velocity, dt):
    avoidance_force = np.zeros(3)
    if len(obstacles) > 0:
        for obstacle in obstacles:
            avoidance_force += obstacle * (max_force / np.linalg.norm(obstacle))
        avoidance_force -= current_velocity
        avoidance_force_norm = np.linalg.norm(avoidance_force)
        if avoidance_force_norm != 0:
            avoidance_force_normalized = avoidance_force / avoidance_force_norm
        else:
            avoidance_force_normalized = avoidance_force
    else:
        avoidance_force_normalized = np.zeros(3)  # If no obstacles, return zero force
    return avoidance_force_normalized

def apply_force(client, force):
    client.moveByVelocityAsync(force[0], force[1], force[2], 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()

client = airsim.MultirotorClient()
client.confirmConnection()

pid_controller = PIDController(kp, kd, ki)

while True:
    start_time = time.time()

    lidar_data = get_lidar_data(client)
    obstacles = process_lidar_data(lidar_data)
    current_velocity = client.getMultirotorState().kinematics_estimated.linear_velocity

    avoidance_force = avoid_obstacles(obstacles, current_velocity.to_numpy_array(), time.time() - start_time)

    thrust = pid_controller.update(np.linalg.norm(avoidance_force), time.time() - start_time)
    avoidance_force_normalized = avoidance_force / np.linalg.norm(avoidance_force)
    force = avoidance_force_normalized * thrust
    apply_force(client, force)

    time.sleep(0.1)
