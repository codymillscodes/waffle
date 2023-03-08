import pymongo
from config import MONGO_USER, MONGO_PASS

client = pymongo.MongoClient(
    f"mongodb+srv://waffle:5oaw7kQStm7pcd0P@waffle.i2tnxdm.mongodb.net/?retryWrites=true&w=majority"
)


class DB:
    def __init__(self):
        self.db = client["waffle"]
        self.queue = self.db["queue"]
        self.users = self.db["users"]

    async def get_queue(self):
        return self.queue.find({})

    async def get_active_queue(self):
        return self.queue.find({"status": "active"})

    async def add_to_queue(self, data):
        self.queue.insert_one(data)

    async def get_twitchers(self):
        pass
