from pymongo import MongoClient

from config import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_PASSWORD,
    MONGO_USERNAME,
    MONGO_DATABASE,
)


class NoSqlAdapter:
    def __init__(self) -> None:
        self.client = MongoClient(
            host=MONGO_HOST,
            port=int(MONGO_PORT),
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authSource="admin",
        )
        self.database = self.client[MONGO_DATABASE]
