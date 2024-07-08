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

hideout_names = ["Vents", "Security", "Lavatory", "Stash", "Generator", "Heating", "Water Collector", "Medstation", "Nut Unit", "Rest Space", "Workbench", "Int. Center", "Shooting Range", "Library", "Scav Case", "Illumination", "Hall of Fame", "Air Filtering Unit", "Solar Power", "Booze Generator", "BTC Farm", "Xmas Tree", "Broken Wall", "Gym", "W"]
# Usage
# json_profiles = get_json_from_server()
# if json_profiles:
#     # Process the profiles as needed
#     print(json_profiles)
# else:
#     print("Failed to retrieve JSON data.")
with open("punch.json", encoding="utf-8") as f:
    profile = json.load(f)
with open("../tarkov_db/simple_items.json", encoding="utf-8") as f:
    items = json.load(f)
with open("../tarkov_db/simple_hideout.json", encoding="utf-8") as f:
    stations = json.load(f)
with open("../tarkov_db/simple_tasks.json", encoding="utf-8") as f:
    tasks = json.load(f)

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
    for i in insurance:
        print(convert_time(i["scheduledTime"]))
        print(len(i["items"]), "items")
        for item in i["items"]:
            if item["slotId"] == "hideout":
                for key, value in items.items():
                    if key == item["_tpl"]:
                        print(value)

def hideout(profile):
    # map index to station
    hideout_names = ["Vents", "Security", "Lavatory", "Stash", "Generator", "Heating", "Water Collector", "Medstation", "Nutrition Unit", "Rest Space", "Workbench", "Intelligence Center", "Shooting Range", "Library", "Scav Case", "Illumination", "Hall of Fame", "Air Filtering Unit", "Solar Power", "Booze Generator", "Bitcoin Farm", "Christmas Tree", "Defective Wall", "Gym", "Weapon Rack", "Weapon Rack"]

    hideout = profile["characters"]["pmc"]["Hideout"]
    for area in hideout["Areas"]:
        # look up each area requirement in hideout.json
        for station in stations:
            if hideout_names[area["type"]] == station:
                print(f"\nL{area["level"]} {station}\n--------")
                level = str(area["level"] + 1)
                #print(station[level])
                try:
                    if stations[station][level]["stationLevelRequirements"]:
                        print("Stations:")
                        for req in stations[station][level]["stationLevelRequirements"]:
                            print(f"L{req['level']} {req['station']}")
                    if stations[station][level]["skillRequirements"]:
                        print("\nSkills:")
                        for req in stations[station][level]["skillRequirements"]:
                            print(f"L{req['level']} {req['name']}")
                    if stations[station][level]["traderRequirements"]:
                        print("\nTraders:")
                        for req in stations[station][level]["traderRequirements"]:
                            print(f"LL{req['level']} {req['name']}")
                    if stations[station][level]["itemRequirements"]:
                        print("\nItems:")
                        for req in stations[station][level]["itemRequirements"]:
                            print(f"{req['count']}x {req['item']}")
                except:
                    print("Complete")


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
                            #print(items[""])

hideout(profile)