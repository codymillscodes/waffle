# https://docs.alldebrid.com
from bot import Waffle
from utils.connection import Connection as Conn
from utils.urls import Urls
from loguru import logger


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


def eval_pick(pick):
    # pick will be one number, a range of numbers('1-5'), or a list of numbers('1,2,3,4,5')
    # need to return a list of numbers
    pick_list = []
    if pick.isdigit():
        pick_list.append(int(pick) - 1)
    elif "-" in pick:
        start, end = pick.split("-")
        pick_list.extend(range(int(start - 1), int(end - 1)))
    elif "," in pick:
        pick_list.extend([int(x) - 1 for x in pick.split(",")])
    logger.info(pick_list)
    return pick_list
