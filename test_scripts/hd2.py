import requests

# https://helldivers-2.fly.dev/api/swaggerui#/
OFFICIAL_STATUS = "https://api.live.prod.thehelldiversgame.com/api/WarSeason/801/Status"
OFFICIAL_INFO = "https://api.live.prod.thehelldiversgame.com/api/WarSeason/801/WarInfo"
r = requests.get(OFFICIAL_INFO)

print(r.text)
with open("info.json", "w") as f:
    f.write(r.text)
