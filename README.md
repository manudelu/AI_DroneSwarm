# Complete Installation and Setup

Step 1: Install Unreal Engine
----------------
Go to the Epic Games store and download `Unreal Engine 5.2`

`Note`: Colosseum doesn't work for versions of Unreal Engine < 5.0. Also, at the time of the creation of this repository it does not work for Unreal Engine 5.3, hence we opted for Unreal Engine 5.2

Step 2: Build Colosseum
----------------

* Install `Visual Studio 2022`. Make sure to select Desktop Development with C++ and the latest version of Windows 10 SDK. Also the latest .NET Framework SDK under the 'Individual Components' tab.
* Start Developer Command Prompt for VS 2022.
* Clone the repo: git clone https://github.com/CodexLabsLLC/Colosseum.git, and go the AirSim directory by cd AirSim.
* Run build.cmd from the command line. This will create ready to use plugin bits in the Unreal\Plugins folder that can be dropped into any Unreal project.

Step 3: Creating and Setting Up Unreal Environment
---------------------

For this step you can follow the official documentation of Airsim: https://microsoft.github.io/AirSim/unreal_custenv/




