import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "librarydb")

client: AsyncIOMotorClient | None = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_URI)

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    if not client:
        raise RuntimeError("MongoDB client is not initialized. Call connect_to_mongo first.")
    return client[MONGO_DB]
