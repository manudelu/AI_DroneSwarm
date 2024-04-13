# AI Drone Swarm

Complete Installation - Colosseum with Unreal Engine 5.2 and ROS from WSL2
=============================

Step 1: Install Unreal Engine
----------------
Go to the Epic Games store and download `Unreal Engine 5.2`

`Note`: Colosseum requires Unreal Engine 5.0 or higher. Currently, it does not support Unreal Engine 5.3.

Step 2: Build Colosseum
----------------

* Install `Visual Studio 2022`. Make sure to select `Desktop Development with C++` and the latest version of `Windows 10 SDK`. Also, under 'Individual Components' tab, select the latest version of `.NET Framework SDK`.
* Start Developer Command Prompt for VS 2022.
* Clone the repository: 
```
git clone https://github.com/CodexLabsLLC/Colosseum.git`
cd Colosseum.
```
* Run `build.cmd` from the command line. This will create ready to use plugin bits in the `Colosseum/Unreal/Plugins` folder that can be dropped into any Unreal project.

Step 3: Creating and Setting Up Unreal Environment
---------------------

Follow the official documentation of AirSim [here](https://microsoft.github.io/AirSim/unreal_custenv/) for setting up the Unreal environment.

Step 4: ROS Noetic Installation on WSL2
--------------------

Follow the tutorial [here](https://github.com/ishkapoor2000/Install_ROS_Noetic_On_WSL?tab=readme-ov-file) for installing ROS Noetic on WSL2.

Step 5: ROS Wrapper
----------------

If your default GCC version is not 8 or above (check using `gcc --version`) on the Ubuntu terminal:
* Install gcc >= 8.0.0: `sudo apt-get install gcc-8 g++-8`
* Verify installation by `gcc-8 --version`

For Ubuntu 20.04:
* Install tf2 sensor and mavros packages: `sudo apt-get install ros-noetic-tf2-sensor-msgs ros-noetic-tf2-geometry-msgs ros-noetic-mavros*`
* Install catkin_tools: `pip install "git+https://github.com/catkin/catkin_tools.git#egg=catkin_tools"`


Clone the Colosseum repository and build it:
```
git clone https://github.com/Microsoft/Colosseum.git;
cd AirSim;
./setup.sh;
./build.sh;
```

Add the source command to your .bashrc for convenience:
```
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Build ROS package:
```
cd ros;
catkin build; # or catkin_make
```

Launch the node:
```
source devel/setup.bash;
roslaunch airsim_ros_pkgs airsim_node.launch;
```

Step 6: Test the Bridge between ROS and Unreal Engine
------------------

* Obtain your IPV4 Address from Windows settings -> Network and Internet -> Properties.
* In the `Documents/AirSim/settings.json` file on Windows, replace "hostname" with your IPV4 Address. Or you can copy and paste this:
```
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "LocalHostIp": "hostname",
  "ApiServerPort": 41541,
  "Vehicles": {
    "Drone": {
      "VehicleType": "SimpleFlight"
    }
  }
}
```
* In the Ubuntu terminal, navigate to `<your_workspace>/src/AirSim/ros/src/launch` and open `airsim_node.launch`, replacing "hostname" with your IPV4 Address.
* Navigate to `Colosseum/Unreal/Environments/Blocks` on Windows and double-click on `Blocks.uproject` to open the test project in Unreal Engine.

`Note`: In the content browser, click on Settings and tick "Show Plugin Content". Also, in Edit -> Editor Preferences, type "cpu" in the search bar and untick "Use Less CPU when in Background" for a smoother experience.

Finally, run the simulation in Unreal Engine, and then, in the Ubuntu terminal, execute: 
```
roslaunch airsim_ros_pkgs airsim_node.launch output:=screen
```
This will launch the ROS node and establish communication with Unreal Engine for testing. If there is no error, then you are all set!

Project 
==============

Download our project from ....

Now that everything is set, download and install the Cesium plugin from the Epic Games Marketplace. Open the project in Unreal Engine, activate the Cesium plugin in plugin settings and restart Unreal Engine.

Run this and that from terminal ....
















