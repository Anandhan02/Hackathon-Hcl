from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client = None
_db = None

async def connect_to_mongo():
    global _client, _db
    _client = AsyncIOMotorClient(settings.MONGO_URI)
    _db = _client[settings.MONGO_DB]
    print(" Connected to MongoDB")

async def close_mongo_connection():
    global _client
    if _client:
        _client.close()
        print(" MongoDB connection closed")

def get_db():
    """Return the active MongoDB database instance."""
    if _db is None:
        raise ConnectionError(" Database not connected. Call connect_to_mongo() first.")
    return _db
