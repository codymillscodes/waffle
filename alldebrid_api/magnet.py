from alldebrid_api import debrid_url
import requests


def upload_magnet(magnet, agent, api_key):
    try:
        r = requests.get(
            debrid_url.create("upload", magnet=magnet, agent=agent, api_key=api_key),
            timeout=30,
        ).json()
        magnet_info = [
            r["data"]["magnets"][0]["id"],
            r["data"]["magnets"][0]["name"],
            r["data"]["magnets"][0]["ready"],
        ]
        return magnet_info
    except KeyError:
        print(r)
        return r["error"]["message"]


def get_all_magnet_status(agent, api_key):
    r = requests.get(
        debrid_url.create("status", agent=agent, api_key=api_key), timeout=30
    ).json()
    if len(r["data"]["magnets"]) <= 0:
        return 0
    else:
        return r["data"]["magnets"]


def get_magnet_status(magnetid, agent, api_key):
    try:
        r = requests.get(
            debrid_url.create(
                "status", magnetid=magnetid, agent=agent, api_key=api_key
            ),
            timeout=30,
        ).json()
        return r["data"]["magnets"]["status"]
    except KeyError:
        return r["error"]["message"]


def delete_magnet(magnetid, agent, api_key):
    try:
        r = requests.get(
            debrid_url.create(
                "delete", magnetid=magnetid, agent=agent, api_key=api_key
            ),
            timeout=30,
        ).json()
        return r["data"]["message"]
    except KeyError:
        return r["error"]["message"]


def restart_magnet(magnetid):
    pass


def instant_magnet(magnet, agent, api_key):
    return requests.get(
        debrid_url.create("instant", magnet=magnet, agent=agent, api_key=api_key),
        timeout=30,
    ).json()["data"]["magnets"][0]["instant"]
