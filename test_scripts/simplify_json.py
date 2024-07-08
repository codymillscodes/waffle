import json

with open("../tarkov_db/tdb_items.json", encoding="utf-8") as f:
    items = json.load(f)
# with open("../tarkov_db/tdb_hideout.json", encoding="utf-8") as f:
#     areas = json.load(f)

def rebuild_items():
    with open("../tarkov_db/tdb_items.json", encoding="utf-8") as f:
        items = json.load(f)
    
    new_json = {}

    for i in items["items"]:
        new_json[i["id"]] = i["name"]

    with open ("../tarkov_db/new_items.json", "w", encoding="utf-8") as f:
        json.dump(new_json, f)

def rebuild_hideout():
    with open("../tarkov_db/tdb_hideout.json", encoding="utf-8") as f:
        areas = json.load(f)

    new_json = {}

    for a in areas["hideoutStations"]:
        new_json[a["name"]] = {}
        for l in a["levels"]:
            level_info =  { "itemRequirements": [
                        {
                            "item": req["item"]["name"],
                            "count": req["count"]
                        }
                        for req in l.get("itemRequirements", [])
                    ],
                    "stationLevelRequirements": [
                        {
                            "station": req["station"]["name"],
                            "level": req["level"]
                        }
                        for req in l.get("stationLevelRequirements", [])
                    ],
                    "skillRequirements": [
                        {
                            "name": req["name"],
                            "level": req["level"]
                        }
                        for req in l.get("skillRequirements", [])
                    ],
                    "traderRequirements": [
                        {
                            "name": req["trader"]["name"],
                            "level": req["value"]
                        }
                        for req in l.get("traderRequirements", [])
                    ]
                }
            new_json[a["name"]][l["level"]] = level_info

    with open("../tarkov_db/simple_hideout.json", "w", encoding="utf-8") as f:
        json.dump(new_json, f)

def rebuild_tasks():
    with open("../tarkov_db/tasks.json", encoding="utf-8") as f:
        tasks = json.load(f)

    new_json = {}
    for t in tasks["tasks"]:
        new_json[t["id"]] = {"name": t["name"], "trader": t["trader"]["name"]}
        try:
            new_json[t["id"]]["map"] = t["map"]["name"]
        except:
            new_json[t["id"]]["map"] = "any"
        new_json[t["id"]]["objectives"] = []
        for o in t["objectives"]:
            new_json[t["id"]]["objectives"].append({"id": o["id"], "description": o["description"]})
    with open("../tarkov_db/simple_tasks.json", "w", encoding="utf-8") as f:
        json.dump(new_json, f)
# rebuild_items()
rebuild_hideout()
# rebuild_tasks()