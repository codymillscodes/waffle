from strings.urls import Urls
import httpx
from loguru import logger
import os
from datetime import datetime


async def upload_magnet(magnet):
    try:
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.DEBRID_UPLOAD + magnet)
        r = r.json()
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
    async with httpx.AsyncClient() as resp:
        r = await resp.get(Urls.DEBRID_STATUS_ACTIVE)
    return r.json()["data"]["magnets"]


async def get_all_magnet_status():
    async with httpx.AsyncClient() as resp:
        r = await resp.get(Urls.DEBRID_STATUS)
    r = r.json()
    if len(r.json["data"]["magnets"]) <= 0:
        return 0
    return r["data"]["magnets"]


async def get_magnet_status(magnetid):
    try:
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.DEBRID_STATUS_ONE + magnetid)
        r = r.json()
        return r["data"]["magnets"]["status"]
    except KeyError:
        return r["error"]["message"]


async def delete_magnet(magnetid):
    try:
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.DEBRID_DELETE + str(magnetid))
        r = r.json()
        return r["data"]["message"]
    except KeyError:
        return r["error"]["message"]


async def instant_magnet(magnet):
    async with httpx.AsyncClient() as resp:
        r = await resp.get(Urls.DEBRID_DELETE + magnet)
    r = r.json()
    return r["data"]["magnets"][0]["instant"]


def eval_pick(pick):
    # pick will be one number, a range of numbers('1-5'), or a list of numbers('1,2,3,4,5')
    # need to return a list of numbers
    pick_list = []
    if pick.isdigit():
        pick_list.append(int(pick.strip()) - 1)
    elif "-" in pick:
        start, end = pick.split("-")
        pick_list.extend(range(int(start.strip()) - 1, int(end.strip())))
    elif "," in pick:
        pick_list.extend([int(x) - 1 for x in pick.replace(" ", "").split(",")])
    logger.info(pick_list)
    return pick_list


async def get_tiktok_link(url):
    logger.info("Getting TikTok link")
    try:
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.DEBRID_UNLOCK + url)
        logger.info(url)
        file_id = r.json()["data"]["id"]
        logger.info(f"TT File ID: {file_id}")
        logger.info(r["data"])
        if r["data"]["link"] == "":
            logger.info("No link found, getting streaming link")
            streams = r["data"]["streams"]

            logger.info(file_id, streams)
            for s in streams:
                logger.info(s)
                if "h264" in s["format"]:
                    logger.info("Found h264")
                    stream_id = s["id"]
                    stream_fs = s["filesize"]
                    break
            else:
                logger.info("Couldn't find h264")
                return 0
            # else:
            #     logger.info("Couldnt find h264")
            #     return 0

            async with httpx.AsyncClient() as resp:
                r = await resp.get(
                    f"{Urls.DEBRID_STREAMING}{file_id}&stream={stream_id}"
                )
                r = r.json()
                logger.info(r)

            if stream_fs >= 25214400:
                logger.info("File too large")
                return 0

        stream_fn = datetime.strftime(datetime.now(), "%m%d%y%H%M%S")

        logger.info(r["data"]["link"])
        return {"url": r["data"]["link"], "fn": stream_fn, "status": 0}
        # download_tiktok_video(r["data"]["link"])

    except Exception as e:
        logger.exception(e)


async def download_tiktok_video(url):
    logger.info("Downloading TikTok video")
    async with httpx.AsyncClient() as resp:
        r = resp.get(url["url"])
        logger.info(r.status)
        if r.status == 200:
            logger.info("Writing to file")
            with open(f"tiktok/{url['fn']}.mp4", "wb") as f:
                async for data in resp.content.iter_chunked(1024):
                    f.write(data)
                    url["status"] = 1
    return url


async def delete_file(file):
    try:
        os.remove(file)
        return True
    except Exception as e:
        logger.exception(e)
        return False
