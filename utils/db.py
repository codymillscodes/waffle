import pymongo
from config import MONGO_USER, MONGO_PASS

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@waffle.i2tnxdm.mongodb.net/?retryWrites=true&w=majority"
)


class DB:
    def __init__(self):
        self.db = client["waffle"]
        self.queue = self.db["queue"]
        self.users = self.db["users"]

    # async def get_queue(self):
    #    return self.queue.find({})

    async def get_active_queue(self):
        return self.queue.find({"status": "active"})

    async def add_to_queue(self, d):
        data = {
            "task_id": d[0],
            "task_name": d[1],
            "user_id": d[2],
            "$currentDate": {"created_at": {"type": "timestamp"}},
            "status": "active",
            "type": d[3],
            "completed_at": "",
        }
        self.queue.insert_one(data)

    async def set_status(self, task_id, status):
        self.queue.update_one(
            {"task_id": task_id},
            {
                "$set": {"status": status},
                "$currentDate": {"completed_at": {"type": "timestamp"}},
            },
        )

    async def get_twitchers(self):
        pass
