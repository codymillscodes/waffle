from utils.urls import Azura
from loguru import logger
from utils.connection import Connection as Conn
import aiohttp


async def get_api_status():
    async with Conn() as resp:
        api_status = await resp.get_json(Azura.GET_API_STATUS)

    return api_status


async def get_cpu_stats():
    async with Conn() as resp:
        cpu_stats = await resp.get_json(Azura.GET_CPU_STATS)

    return cpu_stats


async def get_station_status():
    async with Conn() as resp:
        station_status = await resp.get_json(Azura.GET_STATION_STATUS)

    return station_status


async def restart_station():
    async with Conn() as resp:
        # headers =
        restart = await resp.post_json(Azura.RESTART_STATION)

    return restart


async def get_now_playing():
    async with Conn() as resp:
        now_playing = await resp.get_json(Azura.GET_NOW_PLAYING)

    return now_playing


async def get_requests():
    async with Conn() as resp:
        requests = await resp.get_json(Azura.GET_REQUESTS)

    return requests


async def send_request(request_id):
    async with Conn() as resp:
        # headers =
        request = await resp.post_json(Azura.SEND_REQUEST + str(request_id))

    return request


async def get_playback_history():
    async with Conn() as resp:
        playback_history = await resp.get_json(Azura.GET_PLAYBACK_HISTORY)

    return playback_history


async def get_listeners():
    async with Conn() as resp:
        listeners = await resp.get_json(Azura.GET_LISTENERS)

    return listeners


async def get_queue():
    async with Conn() as resp:
        queue = await resp.get_json(Azura.GET_QUEUE)

    return queue


async def delete_queue_item(queue_item):
    async with Conn() as resp:
        item = await resp.post_json(Azura.DELETE_QUEUE_ITEM + str(queue_item))

    return item


async def send_file(path):
    async with Conn() as resp:
        sent_file = await resp.post_json(Azura.SEND_FILE)

    return sent_file
