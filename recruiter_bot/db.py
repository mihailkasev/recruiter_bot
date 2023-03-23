import logging
import os
from motor import motor_asyncio

from settings import file_handler, stream_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class Database:

    def __init__(self):
        client = motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO"), 27017)
        self.db = client["RecruiterBot"]
        self.users = self.db["Users"]

    async def get_user(self, chat_id):
        user = await self.users.find_one({"chat_id": chat_id})
        if user is not None:
            return user
        user = {
            "chat_id": chat_id,
            "is_passed": False,
            "is_admin": False,
            "is_exported": False,
            "question_id": 0
        }
        await self.users.insert_one(user)
        if str(chat_id) == os.getenv("ADMIN_ID"):
            await self.set_user(chat_id, {"is_admin": True})
        return user

    async def set_user(self, chat_id, update):
        await self.users.update_one({"chat_id": chat_id}, {"$set": update})


db = Database()
