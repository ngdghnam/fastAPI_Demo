from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from config.configuration import settings

# Use AsyncIOMotorClient for async MongoDB operations
client = AsyncIOMotorClient(settings.DB_URL)

db = client["fastAPIDatabase"]

# Use async collections
productCollection = db["products"]
userCollection = db["users"]

# Use AsyncIOMotorGridFSBucket for async GridFS
fs = AsyncIOMotorGridFSBucket(db)
