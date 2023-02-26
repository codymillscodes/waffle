# https://docs.alldebrid.com
from bot import Waffle
from utils.connection import Connection as Conn
from utils.urls import Urls


async def upload_magnet(magnet):
    try:
        async with Conn() as resp:
            r = await resp.get_json(Urls.DEBRID_UPLOAD + magnet)
        magnet_info = [
            r["data"]["magnets"][0]["id"],
            r["data"]["magnets"][0]["name"],
            r["data"]["magnets"][0]["ready"],
        ]
        return magnet_info
    except KeyError:
        print(r)
        return r["error"]["message"]


async def get_active_magnets():
    async with Conn() as resp:
        r = await resp.get_json(Urls.DEBRID_STATUS_ACTIVE)
    return r["data"]["magnets"]


async def get_all_magnet_status():
    async with Conn() as resp:
        r = await resp.get_json(Urls.DEBRID_STATUS)
    if len(r["data"]["magnets"]) <= 0:
        return 0
    else:
        return r["data"]["magnets"]


async def get_magnet_status(magnetid):
    try:
        async with Conn() as resp:
            r = await resp.get_json(Urls.DEBRID_STATUS_ONE + magnetid)
        return r["data"]["magnets"]["status"]
    except KeyError:
        return r["error"]["message"]


async def delete_magnet(magnetid):
    try:
        async with Conn() as resp:
            r = await resp.get_json(Urls.DEBRID_DELETE + magnetid)
        return r["data"]["message"]
    except KeyError:
        return r["error"]["message"]


def restart_magnet(magnetid):
    pass


async def instant_magnet(magnet):
    async with Conn() as resp:
        r = await resp.get_json(Urls.DEBRID_DELETE + magnet)
    return r["data"]["magnets"][0]["instant"]
