"""Configures the Mongo database and provides the database connections.

The code uses the MONGO_PRIVATE_URL environment variable to connect to the
Mongo database. The url is only accessible from within the docker network.

The module exports the following:
    - db: The Mongo database client
    - account_collection: The Mongo database collection for accounts
    - recovery_token_collection: The Mongo database collection for recovery tokens
    - confirm_token_collection: The Mongo database collection for confirmation tokens
    - pwd_context: The passlib password hashing context

"""

import os

from passlib.context import CryptContext
from pymongo import MongoClient


mongo_private_url = os.environ.get("MONGO_PRIVATE_URL")

client = MongoClient(mongo_private_url)

db = client["melomap"]

account_collection = db["accounts"]

recovery_token_collection = db["recovery_tokens"]
confirm_token_collection = db["confirm_tokens"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

