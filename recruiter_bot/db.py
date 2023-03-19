import logging
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from settings import file_handler, stream_handler
from admin_handlers.static_text import logger_connection_err


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class Database:

    def __init__(self):
        client = MongoClient(os.getenv("MONGO"), 27017)
        self.db = client["RecruiterBot"]
        try:
            self.db.command('ping')
        except ServerSelectionTimeoutError:
            logger.error(logger_connection_err)
        self.users = self.db["Users"]

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})
        if user is not None:
            return user
        user = {
            "chat_id": chat_id,
            "is_passed": False,
            "is_admin": False,
            "is_exported": False,
            "question_id": 0
        }
        self.users.insert_one(user)
        if str(chat_id) == os.getenv("ADMIN_ID"):
            self.set_user(chat_id, {"is_admin": True})
        return user

    def set_user(self, chat_id, update):
        self.users.update_one({"chat_id": chat_id}, {"$set": update})


db = Database()
