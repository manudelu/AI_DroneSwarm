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

If your default GCC version is not 8 or above (check using `gcc --version`) on the Ubuntu terminal.
* Install gcc >= 8.0.0: `sudo apt-get install gcc-8 g++-8`
* Verify installation by `gcc-8 --version`

Ubuntu 20.04
* Install tf2 sensor and mavros packages: `sudo apt-get install ros-noetic-tf2-sensor-msgs ros-noetic-tf2-geometry-msgs ros-noetic-mavros*`
* Install catkin_tools: `pip install "git+https://github.com/catkin/catkin_tools.git#egg=catkin_tools"`









