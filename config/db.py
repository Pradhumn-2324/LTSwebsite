from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

conn = MongoClient("mongodb://localhost:27017/")
db = conn["Pradhumn_LTS"]
users_collection = db["Admin_cred"]
