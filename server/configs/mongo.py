from passlib.context import CryptContext
from pymongo import MongoClient
import os


mongo_private_url = os.environ.get("MONGO_PRIVATE_URL")

client = MongoClient(mongo_private_url)

db = client["melomap"]

account_collection = db["accounts"]

recovery_token_collection = db["recovery_tokens"]
confirm_token_collection = db["confirm_tokens"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

