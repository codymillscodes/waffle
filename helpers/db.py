import pymongo
from config import MONGO_USER, MONGO_PASS
from loguru import logger
from helpers.utils import get_time

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@waffle.i2tnxdm.mongodb.net/?retryWrites=true&w=majority"
)


class DB:
    def __init__(self):
        self.client = client["waffle"]
        self.queue = self.client["queue"]
        self.users = self.client["users"]
        self.reco = self.client["reco"]
        self.remind = self.client["reminders"]
        self.theforest = self.client["theforest"]
        self.playlist = self.client["playlist"]

    # async def get_queue(self):
    #    return self.queue.find({})
    async def get_playlist(self):
        return self.playlist.find({})

    async def find_track(self, uri):
        count = self.playlist.count_documents({"uri": uri})
        found = count > 0
        logger.info(f"Found bool: {found}, count: {count}")
        return not found

    async def set_status(self, task_id, status):
        r = self.queue.update_many(
            {"task_id": task_id},
            {
                "$set": {"status": status, "updated_at": get_time()},
            },
        )
        logger.info(
            f"Matched: {r.matched_count}, Modified: {r.modified_count}, acknowledged: {r.acknowledged}"
        )
        logger.info(f"Set status of {task_id} to {status}")

    async def add_to_playlist(self, tracks: list):
        for track in tracks:
            data = {
                "name": track,
                "uri": tracks[track],
            }
            r = self.playlist.insert_one(data)
        logger.info(f"Added to playlist: {r.inserted_id}")

    async def get_active_queue(self):
        return self.queue.find({"status": "active"})

    async def add_to_queue(self, d):
        data = {
            "task_id": d[0],
            "task_name": d[1],
            "user_id": d[2],
            "updated_at": get_time(),
            "status": "active",
            "type": d[3],
        }
        self.queue.insert_one(data)

    # async def update_count(self):
    #    self.reco.update_one({"name": "count"}, {"$inc": {"count": 1}})
