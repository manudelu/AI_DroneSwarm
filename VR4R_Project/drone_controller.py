import airsim
import time
from astar_algorithm import astar
from enum import Enum, auto

class DroneState(Enum):
    INIT = auto()
    TAKEOFF = auto()
    NAVIGATE = auto()
    RETURN_HOME = auto()
    LAND = auto()
    EMERGENCY_LAND = auto()

class DroneController:
    def __init__(self, client, drone_name, home, waypoints, map_data, target_altitude, obstacle_threshold):
        self.client = client
        self.drone_name = drone_name
        self.home = home
        self.waypoints = waypoints
        self.map_data = map_data
        self.target_altitude = target_altitude
        self.obstacle_threshold = obstacle_threshold
        self.battery_status = 100.0
        self.current_position = home
        self.x_start = self.client.simGetObjectPose(self.drone_name).position.x_val
        self.y_start = self.client.simGetObjectPose(self.drone_name).position.y_val
        self.state = DroneState.INIT

    def get_initial_position(self):
        """
        Retrieve the initial position of the drone.

        Returns:
            tuple: Initial coordinates (x, y).
        """
        initial_pose = self.client.simGetObstaclePose(self.drone_name)
        return (initial_pose.position.x_val, initial_pose.position.y_val)

    def run(self):
        """
        Main loop to control the drone based on its state.
        """
        while self.state != DroneState.LAND:
            if self.state == DroneState.INIT:
                self.init_drone()
            elif self.state == DroneState.TAKEOFF:
                self.takeoff_drone()
            elif self.state == DroneState.NAVIGATE:
                self.navigate_to_waypoints()
            elif self.state == DroneState.RETURN_HOME:
                self.return_home()
            elif self.state == DroneState.EMERGENCY_LAND:
                self.emergency_land()
            time.sleep(1)
        self.land_drone()

    def init_drone(self):
        """
        Initialize the drone by confirming connection, arming, and transitioning to takeoff state.
        """
        try:
            self.client.confirmConnection()
            print(f"{self.drone_name} connected!")
            self.client.enableApiControl(True, self.drone_name)
            print(f"{self.drone_name} arming...")
            self.client.armDisarm(True, self.drone_name)
            time.sleep(1)
            self.state = DroneState.TAKEOFF
        except Exception as e:
            print(f"Failed to initialize drone: {str(e)}")
            self.state = DroneState.LAND

    def takeoff_drone(self):
        """
        Command the drone to take off to the target altitude.
        """
        try:
            self.client.takeoffAsync(vehicle_name=self.drone_name).join()
            time.sleep(1)
            print(f"{self.drone_name} hovering at {abs(self.target_altitude)} meters...")
            self.client.moveToZAsync(self.target_altitude, 2, vehicle_name=self.drone_name).join()
            time.sleep(1)
            self.state = DroneState.NAVIGATE
        except Exception as e:
            print(f"Failed to take off: {str(e)}")
            self.state = DroneState.LAND

    def navigate_to_waypoints(self):
        """
        Navigate the drone through the defined waypoints until low battery or completion.
        """
        for waypoint in self.waypoints:
            try:
                if self.battery_status < 30:
                    self.state = DroneState.RETURN_HOME
                    return
                real_waypoint = (int(waypoint[0] + self.x_start), int(waypoint[1] + self.y_start))
                print(f"{self.drone_name} moving to waypoint {real_waypoint}...")
                path, self.battery_status = astar(self.map_data, self.current_position, waypoint, self.obstacle_threshold, self.battery_status)
                airsim_path = [airsim.Vector3r(x, y, self.target_altitude - self.map_data[(x, y)] + 1) for x, y in path]
                self.client.moveOnPathAsync(airsim_path, velocity=1.5, vehicle_name=self.drone_name, drivetrain=airsim.DrivetrainType.ForwardOnly,
                                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0),
                                            lookahead=-1, adaptive_lookahead=1).join()
                print(f"{self.drone_name} reached waypoint {real_waypoint}.")
                print(f"Remaining battery: {round(self.battery_status)}%")
                self.current_position = waypoint
            except Exception as e:
                print(f"Failed to navigate to waypoint: {str(e)}")
                self.state = DroneState.LAND
                return

        self.state = DroneState.RETURN_HOME

    def return_home(self):
        """
        Command the drone to return to its home position.
        """
        try:
            print(f"{self.drone_name} returning home...")
            path, self.battery_status = astar(self.map_data, self.current_position, self.home, self.obstacle_threshold, self.battery_status)
            if path:
                return_path = [airsim.Vector3r(x, y, self.target_altitude - self.map_data[(x, y)] + 1) for x, y in path]
                self.client.moveOnPathAsync(return_path, velocity=1.5, vehicle_name=self.drone_name, drivetrain=airsim.DrivetrainType.ForwardOnly,
                                            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0),
                                            lookahead=-1, adaptive_lookahead=1).join()
                print(f"{self.drone_name} returned home successfully.")
                print(f"Remaining battery: {round(self.battery_status)}%")
                self.state = DroneState.LAND
            else:
                self.state = DroneState.EMERGENCY_LAND
        except Exception as e:
            print(f"Failed to return home: {str(e)}")
            self.state = DroneState.LAND

    def emergency_land(self):
        """
        Execute emergency landing procedure when battery is critically low.
        """
        try:
            print(f"Battery critically low! {self.drone_name} emergency landing...")
            self.state = DroneState.LAND
        except Exception as e:
            print(f"Failed to execute emergency landing: {str(e)}")

    def land_drone(self):
        """
        Command the drone to land and disarm.
        """
        try:
            self.client.moveToZAsync(-3, 1, vehicle_name=self.drone_name).join()
            time.sleep(1)
            print(f"{self.drone_name} landing...")
            self.client.landAsync(vehicle_name=self.drone_name).join()
            print(f"{self.drone_name} disarming...")
            self.client.armDisarm(False, self.drone_name)
            self.client.enableApiControl(False, self.drone_name)
            print(f"{self.drone_name} done.")
        except Exception as e:
            print(f"Failed to land the drone: {str(e)}")