import requests
import time

# from alldebrid_api import debrid_url
# from alldebrid_api import magnet

agent = ""
api_key = ""
url = f"https://api.alldebrid.com/v4/magnet/status?agent={agent}&apikey={api_key}&status=error"
delete_url = (
    f"https://api.alldebrid.com/v4/magnet/delete?agent={agent}&apikey={api_key}&id="
)


def delete():
    r = requests.get(url).json()["data"]["magnets"]

    mag_slice = []
    for torrent in r:
        mag_slice.append(torrent)

    # mag_slice = mag_slice[-(num):]
    ids = []
    for torrent in r:
        if torrent in mag_slice:
            ids.append(r[torrent]["id"])
    total = len(ids)
    counter = 0
    for i in ids:
        counter = counter + 1
        r = requests.get(f"{delete_url}{i}").json()
        if r["status"] == "success":
            print(f"[{counter}/{total}] {r['data']['message']}")
        else:
            print(f"[{counter}/{total}] Failed to delete {i}")
        time.sleep(0.1)


delete()
