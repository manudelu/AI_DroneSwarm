import airsim
import time

def adjust_altitude(client):
    while True:
        altitude_data = client.getDistanceSensorData(vehicle_name="Drone1")
        altitude = altitude_data.distance
        print(f"Current altitude: {altitude} meters")      
        time.sleep(1)  # Adjust the sleep time as needed

def main():
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # Start continuously retrieving and adjusting altitude information
    adjust_altitude(client)

if __name__ == "__main__":
    main()
