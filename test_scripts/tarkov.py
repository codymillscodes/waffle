from time import strftime, localtime
import subprocess
import json

def get_json_from_server():
    try:
        # Replace with your server details
        ssh_command = "ssh user@your_server_ip 'cat /path/to/your/json/file.json'"
        json_data = subprocess.check_output(ssh_command, shell=True)
        parsed_data = json.loads(json_data.decode('utf-8'))
        return parsed_data
    except Exception as e:
        print(f"Error fetching JSON data: {e}")
        return None

# Usage
json_profiles = get_json_from_server()
if json_profiles:
    # Process the profiles as needed
    print(json_profiles)
else:
    print("Failed to retrieve JSON data.")

## 66386ff80004f76d1cfd1ed0.json  
# 663ceb720002026a171b0976.json  
# 663db4db0002526d025cc220.json
## 6639b6b100046c1b8406b0fa.json  
# 663d3c370004300f278f83fb.json  
# 663dbc0600032a4e81ed657c.json

def convert_time(e):
    return strftime('%Y-%m-%d %H:%M:%S', localtime(e))

def insurance(profile):
    insurance = profile["insurance"]
    insurance_packages = []
    for i in insurance:
        insurance_packages.append(convert_time(i["scheduledTime"]))
        ## deal with items

def hideout(profile):
    # map index to station
    hideout = profile["characters"]["pmc"]["Hideout"]
    for a in hideout["Areas"]:
        # look up each area requirement in hideout.json
        # check inventory for needed items
        pass

def tasks(profile):
    tasks = profile["characters"]["pmc"]["Quests"]
    # lookup task name in tasks.json
    for t in tasks:
        if t["status"] == 2:
            conditions = t["completedConditions"]
            for c in conditions:
                for counter in profile["characters"]["pmc"]["TaskConditionCounters"]:
                    if counter["sourceId"] == c:
                        given = counter["value"]
                        # lookup item and quantity