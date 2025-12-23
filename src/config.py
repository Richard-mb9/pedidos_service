from typing import Literal
from decouple import config  # type: ignore
from dotenv import load_dotenv, find_dotenv


ENVIRONMENT: Literal["local", "HML", "DEV", "PRD"] = config(
    "ENVIRONMENT", default="local"
)  # type: ignore
dotenv = find_dotenv(f".env.{ENVIRONMENT.lower()}")
load_dotenv(dotenv)


MQ_HOST = config("MQ_HOST")
MQ_USER = config("MQ_USER")
MQ_PASSWORD = config("MQ_PASSWORD")
MQ_PORT = config("MQ_PORT")


MONGO_HOST = config("MONGO_HOST")
MONGO_USERNAME = config("MONGO_USERNAME")
MONGO_PASSWORD = config("MONGO_PASSWORD")
MONGO_PORT = config("MONGO_PORT")
MONGO_DATABASE = config("MONGO_DATABASE")
