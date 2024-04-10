#!/usr/bin/env python

import rospy
import math
import pymap3d as pm

from tf.transformations import euler_from_quaternion

from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from airsim_ros_pkgs.msg import VelCmd, GPSYaw
from drone_coverage_msgs.msg import DroneGoalPose


class Object :
    pass


class PidDroneController :

    def __init__(self) :
        # Initializing this node
        rospy.init_node("drone_pid_controller")
        # Initializing other variables
        self._has_home = False
        self._has_odom = False
        self._reached_goal = True
        self._is_halting = False
        self._prev_error = Object()
        self._current_pose = Object()
        self._home_pose = Object()
        self._goal_pose = Object()
        # Loading all the private parameters for this controller
        self._load_pid_params()
        #self._load_dynamic_constraints()
        # Initializing the errors
        self._reset_errors()
        # Creating interfaces for ros communcation
        self._create_ros_interfaces()
        # Creating a timer for handling the update of the velocity
        rospy.Timer(rospy.Duration(self._update_period_sec), self._update_drone_velocity)


    def _load_pid_params(self):
        # Loading the vehicle name this controller is referred to
        self._drone_name = rospy.get_param("~drone_name")
        # Loading all the parameters for the pid controller
        self._kp_x = rospy.get_param("~kp_x")
        self._kp_y = rospy.get_param("~kp_y")
        self._kp_z = rospy.get_param("~kp_z")
        self._kp_yaw = rospy.get_param("~kp_yaw")
        self._kd_x = rospy.get_param("~kd_x")
        self._kd_y = rospy.get_param("~kd_y")
        self._kd_z = rospy.get_param("~kd_z")
        self._kd_yaw = rospy.get_param("~kd_yaw")
        self._goal_xyz_threshold = rospy.get_param("~goal_xyz_threshold")
        self._goal_yaw_threshold = rospy.get_param("~goal_yaw_threshold")
        self._update_period_sec = rospy.get_param("~update_perdiod_sec")


    def _load_dynamic_constraints(self):
        # Loading all the parameters for the dynamic constraints
        self._max_vel_horz = rospy.get_param("/drone_max_vel_horz")
        self._max_vel_vert = rospy.get_param("/drone_max_vel_vert")
        self._max_vel_rotz = rospy.get_param("/drone_max_vel_rotz")


    def _reset_errors(self) :
        # Resetting all the errors related to the goal
        self._prev_error.x = 0.0
        self._prev_error.y = 0.0
        self._prev_error.z = 0.0
        self._prev_error.yaw = 0.0
    

    def _create_ros_interfaces(self):
        # Creating a Subscriber for the drone gps
        self._gps_sub = rospy.Subscriber(
            "/airsim_node/"+self._drone_name+"/global_gps", NavSatFix, queue_size=1,
            callback=self._on_drone_gps_message 
        )
        # Creating a Subscriber for the drone odom
        self._local_odom_sub = rospy.Subscriber(
            "/airsim_node/"+self._drone_name+"/odom_local_ned", Odometry, queue_size=1, 
            callback=self._on_drone_odometry_message
        )
        # Creating a Service for the goal position
        self._goal_msg = rospy.Subscriber(
            "/airsim_node/"+self._drone_name+"/local_goal", DroneGoalPose, 
            callback=self._on_local_goal_message
        )
        # Creating a Service for temporarely halting the drone
        self._alt_sub = rospy.Subscriber(
            "/airsim_node/"+self._drone_name+"/halt", Bool,
            callback=self._on_halt_request_message
        )
        # Creating a Publisher for the drone velocity
        self._vel_pub = rospy.Publisher(
            "/airsim_node/"+self._drone_name+"/vel_cmd_pid_controller", VelCmd, queue_size=1
        )
        # Creating a Publisher for the drone global position
        self._global_odom_pub = rospy.Publisher(
            "/airsim_node/"+self._drone_name+"/odom_global_ned", Odometry, queue_size=1
        )
        # Creating a Publisher for signaling reaching goal
        self._goal_state_msg = rospy.Publisher(
            "/airsim_node/"+self._drone_name+"/goal_state", Bool, queue_size=1, latch=True
        )


    def _on_drone_gps_message(self, msg):
        # Computing the current position in ned coordinates
        home = pm.geodetic2ned(msg.latitude, msg.longitude, msg.altitude, 0, 0, 0)
        # Storing the home position and unregistering
        self._has_home = True
        self._home_pose = Object()
        self._home_pose.x = home[0]
        self._home_pose.y = home[1]
        self._home_pose.z = home[2]
        self._home_pose.yaw = 0.0
        self._gps_sub.unregister()
        # Debugging
        ix = "{:.2f}".format(home[0])
        iy = "{:.2f}".format(home[1])
        iz = "{:.2f}".format(home[2])
        rospy.loginfo("[PID "+self._drone_name+"] Obtained initial position at [x:"+ix+" y:"+iy+ " z:"+iz+"]!")


    def _on_drone_odometry_message(self, msg):
        # Waiting for the home position before computing current position
        if not self._has_home :
            return
        # Storing the current position and orientation of the drone
        self._current_pose.x = msg.pose.pose.position.x + self._home_pose.x
        self._current_pose.y = msg.pose.pose.position.y + self._home_pose.y
        self._current_pose.z = msg.pose.pose.position.z + self._home_pose.z
        # Converting the quaternion to yaw angles
        quat = msg.pose.pose.orientation
        quat_expl = [quat.x, quat.y, quat.z, quat.w]
        self._current_pose.yaw = euler_from_quaternion(quat_expl)[2]
        # Debugging
        if not self._has_odom :
            rospy.loginfo("[PID "+self._drone_name+"] First odometry received!")
            self._has_odom = True
        # Publishing message with the current global position
        msg.pose.pose.position.x = self._current_pose.x
        msg.pose.pose.position.y = self._current_pose.y
        msg.pose.pose.position.z = self._current_pose.z
        self._global_odom_pub.publish(msg)


    def _on_local_goal_message(self, msg):
        if not self._has_odom :
            return
        # Storing the requested goal position
        self._goal_pose.x = msg.x
        self._goal_pose.y = msg.y
        self._goal_pose.z = -msg.z
        self._goal_pose.yaw = msg.yaw
        # Debugging
        rospy.loginfo("[PID "+self._drone_name+"] Requested goal x:"+str(msg.x)+" y:"+str(msg.y)+ " z:"+str(msg.z))
        # There is a new goal to reach
        self._reached_goal = False
        self._reset_errors()
        self._goal_state_msg.publish(Bool(False))


    def _on_halt_request_message(self, msg):
        # Setting a zero velocity on the drone
        self._vel_pub.publish(VelCmd())
        # Setting the halting mode as requested
        self._is_halting = msg.data


    def _check_goal_reached(self):
        # If the goal has already been reached, do nothing
        if self._reached_goal :
            return
        # Computing the error in the position
        error_x = self._goal_pose.x - self._current_pose.x
        error_y = self._goal_pose.y - self._current_pose.y
        error_z = self._goal_pose.z - self._current_pose.z
        diff_xyz = math.sqrt(error_x*error_x + error_y*error_y + error_z*error_z)
        # Computing the error in the yaw
        diff_yaw = angular_dist(self._current_pose.yaw, self._goal_pose.yaw)
        # Checking the thresholds
        rospy.loginfo("[PID "+self._drone_name+"] distance is "+str(diff_xyz))
        if diff_xyz < self._goal_xyz_threshold and diff_yaw < self._goal_xyz_threshold :
            self._reached_goal = True


    def _update_drone_velocity(self, event):
        # Check if the current position for the drone is available
        if not self._has_home :
            rospy.logwarn_once("[PID "+self._drone_name+"] Waiting for initial position!")
            return
        if not self._has_odom :
            rospy.logwarn_once("[PID "+self._drone_name+"] Waiting for first odometry!")
            return
        # Check if the drone is currently halting
        if self._is_halting or self._reached_goal :
            return
        # Check if the current goal has already been reached
        self._check_goal_reached()
        if self._reached_goal :
            # The goal has just been reached
            self._goal_state_msg.publish(Bool(True))
            rospy.loginfo("[PID "+self._drone_name+"] Goal pose has been reached!")
            return
            
        # Creating the new velocity for the drone
        vel = self._compute_new_velocity()
        self._enforce_dynamic_constraints(vel)
        # Publishing the new velocity
        self._vel_pub.publish(vel)


    def _compute_new_velocity(self):
        # Computing the error between the current pose and target pose
        curr_error = Object()
        curr_error.x = self._goal_pose.x - self._current_pose.x
        curr_error.y = self._goal_pose.y - self._current_pose.y
        curr_error.z = self._goal_pose.z - self._current_pose.z
        curr_error.yaw = angular_dist(self._current_pose.yaw, self._goal_pose.yaw)
        # Computing pid p variables
        p_term_x = self._kp_x * curr_error.x
        p_term_y = self._kp_y * curr_error.y
        p_term_z = self._kp_z * curr_error.z
        p_term_yaw = self._kp_yaw * curr_error.yaw
        # Computing pid d variables
        d_term_x = self._kd_x * self._prev_error.x
        d_term_y = self._kd_y * self._prev_error.y
        d_term_z = self._kd_z * self._prev_error.z
        d_term_yaw = self._kd_yaw * self._prev_error.yaw
        # Storing the current error for the next iteration
        self._prev_error = curr_error
        # Computing the new velocity
        vel = VelCmd()
        vel.twist.linear.x = p_term_x + d_term_x
        vel.twist.linear.y = p_term_y + d_term_y
        vel.twist.linear.z = p_term_z + d_term_z
        vel.twist.angular.z = p_term_yaw + d_term_yaw
        return vel


    def _enforce_dynamic_constraints(self, vel):
        # Computing the magnitude of the horizontal direction of the velocity
        norm_horz = math.sqrt((vel.twist.linear.x * vel.twist.linear.x) + (vel.twist.linear.y * vel.twist.linear.y))
        # Clamping the horizontal velocity
        if norm_horz > self._max_vel_horz :
            vel.twist.linear.x = (vel.twist.linear.x / norm_horz) * self._max_vel_horz 
            vel.twist.linear.y = (vel.twist.linear.y / norm_horz) * self._max_vel_horz
        # Clamping the vertical velocity
        if abs(vel.twist.linear.z) > self._max_vel_vert :
            vel.twist.linear.z = math.copysign(self._max_vel_vert, vel.twist.linear.z)
        # Clamping the rotation velocity
        if abs(vel.twist.angular.z) > self._max_vel_rotz :
            vel.twist.angular.z = math.copysign(self._max_vel_rotz, vel.twist.angular.z)



def wrap_to_pi(radians) :
    m = int(radians / (2 * math.pi))
    radians = radians - m * 2 * math.pi
    if radians > math.pi :
        radians -= 2.0 * math.pi
    elif radians < -math.pi :
        radians += 2.0 * math.pi
    return radians


def angular_dist(from_rads, to_rads):
    from_rads = wrap_to_pi(from_rads)
    to_rads = wrap_to_pi(to_rads)
    return wrap_to_pi(to_rads - from_rads)


if __name__ == "__main__":
    PidDroneController()
    rospy.spin()
