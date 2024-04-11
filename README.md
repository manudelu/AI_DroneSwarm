# AI Drone Swarm

# Complete Installation and Setup

Colosseum with Unreal Engine on Windows
=============================

Step 1: Install Unreal Engine
----------------
Go to the Epic Games store and download `Unreal Engine 5.2`

`Note`: Colosseum doesn't work for versions of Unreal Engine < 5.0. Also, at the time of the creation of this repository it does not work for Unreal Engine 5.3, hence we opted for Unreal Engine 5.2

Step 2: Build Colosseum
----------------

* Install `Visual Studio 2022`. Make sure to select Desktop Development with C++ and the latest version of Windows 10 SDK. Also the latest .NET Framework SDK under the 'Individual Components' tab.
* Start Developer Command Prompt for VS 2022.
* Clone the repo: `git clone https://github.com/CodexLabsLLC/Colosseum.git`, and go to the AirSim directory by `cd AirSim`.
* Run `build.cmd` from the command line. This will create ready to use plugin bits in the `Colosseum/Unreal/Plugins` folder that can be dropped into any Unreal project.

Step 3: Creating and Setting Up Unreal Environment
---------------------

For this step you can follow the official documentation of Airsim: https://microsoft.github.io/AirSim/unreal_custenv/

ROS Noetic Installation on WSL2
==========================

For ROS Noetic installation on WSL2 you can follow this tutorial: https://github.com/ishkapoor2000/Install_ROS_Noetic_On_WSL?tab=readme-ov-file

ROS Wrapper
=================

Setup
------------

If your default GCC version is not 8 or above (check using `gcc --version`) on the Ubuntu terminal.
* Install gcc >= 8.0.0: `sudo apt-get install gcc-8 g++-8`
* Verify installation by `gcc-8 --version`

Ubuntu 20.04
* Install tf2 sensor and mavros packages: `sudo apt-get install ros-noetic-tf2-sensor-msgs ros-noetic-tf2-geometry-msgs ros-noetic-mavros*`
* Install catkin_tools: `pip install "git+https://github.com/catkin/catkin_tools.git#egg=catkin_tools"`

Build 
------------

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

Build ROS package
------------------

```
cd ros;
catkin build; # or catkin_make
```

Running
--------

```
source devel/setup.bash;
roslaunch airsim_ros_pkgs airsim_node.launch;
```

Test the Bridge between ROS and Unreal Engine
===========================

Now, that you are all set go to your Windows settings -> Network and Internet -> Properties -> Copy the IPV4 Address

In Windows go to your `Documents/AirSim` folder, open the `settings.json` file and change it like that (swap "hostname" with your IPV4 Address):

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

Then, in the Ubuntu terminal navigate through your workspace `catkin_ws/src/AirSim/ros/src/launch` and open the `airsim_node.launch` by typing the command: `gedit airsim_node.launch`
Here you have to change "hostname" with your IPV4 Address just like in the previous step.

For testing everything until now, in Windows where you installed Colosseum, you have to navigate through `Colosseum/Unreal/Environments/Blocks` and double-click on the `Blocks_environment.uproject`.
This will open a debug project inside Unreal Engine. Note that in the content browser you'll have to click on the settings icon and tick "Show Plugin Content" and also in project settings you'll have to type cpu in the searchbar and untick the option that will appear to have a smoother experience.
















