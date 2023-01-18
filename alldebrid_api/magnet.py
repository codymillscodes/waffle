from alldebrid_api import debrid_url
import requests


def upload_magnet(magnet):
    try:
        r = requests.get(debrid_url.create("upload", magnet=magnet)).json()
        magnet_info = [
            r["data"]["magnets"][0]["id"],
            r["data"]["magnets"][0]["name"],
            r["data"]["magnets"][0]["ready"],
        ]
        return magnet_info
    except KeyError:
        print(r)
        return r["error"]["message"]


def get_all_magnet_status():
    r = requests.get(debrid_url.create("status")).json()
    if len(r["data"]["magnets"]) <= 0:
        return 0
    else:
        return r["data"]["magnets"]


def get_magnet_status(magnetid):
    try:
        r = requests.get(debrid_url.create("status", magnetid=magnetid)).json()
        return r["data"]["magnets"]["status"]
    except KeyError:
        return r["error"]["message"]


def delete_magnet(magnetid):
    try:
        r = requests.get(debrid_url.create("delete", magnetid=magnetid)).json()
        return r["data"]["message"]
    except KeyError:
        return r["error"]["message"]


def restart_magnet(magnetid):
    pass


def instant_magnet(magnet):
    return requests.get(debrid_url.create("instant", magnet=magnet)).json()["data"][
        "magnets"
    ][0]["instant"]
