import subprocess

def run_drone_script_in_new_terminal(script_name):
    # Command to run the script in a new cmd window
    subprocess.run(["start", "cmd", "/k", "python", script_name], shell=True)

if __name__ == "__main__":
    # Define script names for each drone
    drone_scripts = ["drone1.py", "drone2.py", "drone3.py"]

    # Create a process for each drone script
    for script_name in drone_scripts:
        run_drone_script_in_new_terminal(script_name)