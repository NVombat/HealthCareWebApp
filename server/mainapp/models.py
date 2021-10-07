import pymongo
import os

from dotenv import load_dotenv
load_dotenv()


class UserData:
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = client[os.getenv("MONGO_DB")][os.getenv("DATA_COLLECTION")]

    def insert_user(self, name: str, email: str, password: str) -> None:
        pass

    def validate_user(self, email: str, password: str) -> bool:
        pass
