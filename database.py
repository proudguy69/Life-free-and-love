from pymongo import MongoClient
from discord import Member
import time

client = MongoClient('mongodb://localhost:27017')
database = client.get_database("livefreeandlove")
queue = database.get_collection("queue")

def add_to_queue(member:Member, gender):
    document = {
        "user_id": member.id,
        "queued_at": int(time.time()),
        "gender": gender,
        "status": "in_queue"
    }
    queue.update_one({"user_id": member.id}, {"$set": document}, upsert=True)

def activate_user(member:Member):
    queue.update_one({"user_id": member.id}, {"$set": {"status": "active"}}, upsert=True)
