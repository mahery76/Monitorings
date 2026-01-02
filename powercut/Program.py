import psutil
import time
import json
from datetime import datetime

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery is not None:
        return {
            "plugged": battery.power_plugged,
            "percent": battery.percent,
            "status": "Plugged In" if battery.power_plugged else "Not Plugged In",
            "current_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return {}

battery_data = get_battery_status()

# read the json file and get the data from it
with open('battery_status.json', 'r') as f:
    battery_status_data_list = json.load(f)

battery_status_data_list.append(battery_data)    

# write the file once at the start of the program
with open('battery_status.json', 'w') as f:
    json.dump(battery_status_data_list, f, indent=4)        

def write_battery_data():
    try:
        battery_data = get_battery_status()
        print(battery_data['plugged'])
        # if the current status of the battery is not the same as his last status then dump the json file
        if battery_data['plugged'] != battery_status_data_list[-1]['plugged']:            
            # Append the current battery data to the list
            battery_status_data_list.append(battery_data)
            with open('battery_status.json', 'w') as f:
                json.dump(battery_status_data_list, f, indent=4)
           
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    while True:
        write_battery_data()
        time.sleep(10)
    