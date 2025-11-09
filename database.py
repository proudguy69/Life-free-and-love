from pymongo.asynchronous.mongo_client import AsyncMongoClient
from discord import Member
import time

client = AsyncMongoClient('mongodb://localhost:27017')
database = client.get_database("livefreeandlove")
queue = database.get_collection("queue")

async def add_to_queue(member:Member, gender):
    document = {
        "user_id": member.id,
        "queued_at": int(time.time()),
        "gender": gender,
        "status": "in_queue"
    }
    await queue.update_one({"user_id": member.id}, {"$set": document}, upsert=True)

async def activate_user(member:Member):
    await queue.update_one({"user_id": member.id}, {"$set": {"status": "active"}}, upsert=True)
