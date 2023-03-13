import pymongo
from config import MONGO_USER, MONGO_PASS
from datetime import datetime
from loguru import logger

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@waffle.i2tnxdm.mongodb.net/?retryWrites=true&w=majority"
)


class DB:
    def __init__(self):
        self.client = client["waffle"]
        self.queue = self.client["queue"]
        self.users = self.client["users"]

    # async def get_queue(self):
    #    return self.queue.find({})
    def get_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    async def get_active_queue(self):
        return self.queue.find({"status": "active"})

    async def add_to_queue(self, d):
        data = {
            "task_id": d[0],
            "task_name": d[1],
            "user_id": d[2],
            "updated_at": self.get_time(),
            "status": "active",
            "type": d[3],
        }
        self.queue.insert_one(data)

    async def set_status(self, task_id, status):
        self.queue.update_one(
            {"task_id": task_id},
            {
                "$set": {"status": status, "updated_at": self.get_time()},
            },
        )
        logger.info(f"Set status of {task_id} to {status}")

    async def get_twitchers(self):
        return self.users.find({"twitcher": {"$eq": True}})
