from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = ("mongodb://localhost:27017/")
conn = AsyncIOMotorClient(MONGODB_URL)
db = conn["Pradhumn_LTS"]
users_collection = db["Admin_cred"]


'''
conn = MongoClient("mongodb://localhost:27017/")
db = conn["Pradhumn_LTS"]
users_collection = db["Admin_cred"]
'''
