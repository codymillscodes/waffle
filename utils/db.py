import pymongo
from config import MONGO_USER, MONGO_PASS
from loguru import logger
from utils.helpers import get_time

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

    async def add_to_playlist(self, tracks: list):
        for track in tracks:
            data = {
                "name": track,
                "uri": tracks[track],
            }
            r = self.playlist.insert_one(data)
        logger.info(f"Added to playlist: {r.inserted_id}")

    async def increment_forest_stat(self, user_id):
        pass

    async def add_forest_stat(self, user_id):
        pass

    async def get_forest_stat(self, user_id):
        pass

    async def get_all_forest_stats(self):
        pass

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

    async def get_twitchers(self):
        return self.users.find({"twitcher": {"$eq": True}})

    async def set_twitcher_status(self, user, online: bool):
        r = self.users.update_one({"user": user}, {"$set": {"online": online}})
        logger.info(f"Set twitcher status of {user} to {online}")
        logger.info(f"Matched: {r.matched_count}, Modified: {r.modified_count}")

    async def add_reco(self, reco):
        data = {
            "number": self.reco.count_documents({}) + 1,
            "recommender": reco[0],
            "receiver": reco[1],
            "media type": reco[2],
            "media title": reco[3],
            "rating": 0,
            "consumed": False,
            "timestamp": get_time(),
        }
        r = self.reco.insert_one(data)
        logger.info(f"Added reco: {r.inserted_id}")

    async def get_reco(self, user_id):
        return self.reco.find({"receiver": user_id, "consumed": False})

    async def set_reco_consumed(self, reco_id, rating):
        r = self.reco.update_one(
            {"number": reco_id}, {"$set": {"consumed": True, "rating": rating}}
        )
        logger.info(f"Matched: {r.matched_count}, Modified: {r.modified_count}")
        logger.info(f"Set reco {reco_id} to watched")
        return r.modified_count

    async def get_consumed_reco(self, user_id):
        return self.reco.find({"receiver": user_id, "consumed": True})

    async def add_reminder(self, user_id, time, reminder):
        data = {
            "user_id": user_id,
            "reminder": reminder,
            "reminded": False,
            "time_to_remind": time,
            "timestamp": get_time(),
        }
        r = self.remind.insert_one(data)
        logger.info(f"Added reminder: {r.inserted_id}")

    # async def update_count(self):
    #    self.reco.update_one({"name": "count"}, {"$inc": {"count": 1}})
