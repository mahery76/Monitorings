## Installation

- Install python and go to the root directory of the repo
- run "python Program.py"

## Step guide of the code 
- get the battery status data for once
- read the battery_status.json file
- get the data from this json file
- assign it to battery_status_data_list and append to it the current battery data 
- write the file by dumping battery_status_data_list to the json file for once at the start of the program
- every 10 second: 
. get the current battery data
. if the current status of the battery is not the same as its last status then dump the json file
