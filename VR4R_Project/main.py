import multiprocessing
import subprocess

def run_drone_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    # Define script names for each drone
    drone_scripts = ["drone1.py", "drone2.py", "drone3.py"]

    # Create a process for each drone script
    processes = []
    for script_name in drone_scripts:
        process = multiprocessing.Process(target=run_drone_script, args=(script_name,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
