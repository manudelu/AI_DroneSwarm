# AI Drone Swarm

Complete Installation - Colosseum with Unreal Engine 5.2 and AirSim Python API
=============================

Step 1: Install Unreal Engine 
----------------
Visit the Epic Games store and download `Unreal Engine 5.2`

`Note`: Colosseum requires Unreal Engine 5.0 or higher. Currently, it does not support Unreal Engine 5.3, nor 5.4

Step 2: Build Colosseum
----------------

* Install `Visual Studio 2022`. Make sure to select `Desktop Development with C++` and the latest version of `Windows 10 SDK`. Also, under 'Individual Components' tab, select the latest version of `.NET Framework SDK`.
* Launch Developer Command Prompt for VS 2022.
* Clone the repository: 
```
git clone https://github.com/CodexLabsLLC/Colosseum.git`
cd Colosseum.
```
* Execute `build.cmd` from the command line. This will create ready to use plugin bits in the `Colosseum/Unreal/Plugins` folder that can be dropped into any Unreal project.

Step 3: Creating and Setting Up Unreal Environment
---------------------

Follow the official documentation of AirSim [here](https://microsoft.github.io/AirSim/unreal_custenv/) for setting up the Unreal environment.

Step 4: Install Anaconda 
-----------------------

Visit the official Anaconda website [here](https://www.anaconda.com/) and download it.

Step 5: AirSim API
----------------------

Open `Anaconda Prompt` and install the following packages:
```
pip install msgpack-rpc-python
pip install airsim
```

Step 6: Run the simulation on Blocks Environment
------------

Navigate to the Colosseum installation folder and open the Blocks Environment:
```
.../Colosseum/Unreal/Environments/Blocks/Blocks.uproject
```

Once opened, run the simulation, you should see the drone spawning within the environment. Then, in the terminal, navigate to this directory:
```
.../Colosseum/PythonClient/multirotor
```

Here, try executing the programs to ensure everything is functioning correctly. For instance, type:
```
python hello_drone.py
```

Project Setup
=============================

Download our Unreal Environment, of the `Azienda Agricola Durin` wineyard in `Ortovero (Albenga)`, using this link: [insert link here]

Upon completion, navigate to the designated folder and open the settings.json file located at:
```
Documents/AirSim/settings.json
```

Within this file, insert the following configuration:
```
{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/main/docs/settings.md",
	"SettingsVersion": 1.2,
	"SimMode": "Multirotor",
	"ClockSpeed": 1,
	
	"Vehicles": {
		"Drone1": {
		  "VehicleType": "SimpleFlight",
		  "X": 0, "Y": 0, "Z": 0
		},
		"Drone2": {
		  "VehicleType": "SimpleFlight",
		  "X": 0, "Y": 7, "Z": 0
		},
		"Drone3": {
		  "VehicleType": "SimpleFlight",
		  "X": 0, "Y": 14, "Z": 0
		}
    }
}
```

Once you've opened our project in Unreal Engine and initiated the simulation, proceed to download our repository. Navigate to the `VR4R_Project` directory and execute the following command in the terminal:
```
python main.py
```

This will prompt three additional terminals to appear, each dedicated to a single drone. You'll observe them autonomously navigating within the environment.











