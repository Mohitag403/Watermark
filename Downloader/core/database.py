from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.thumbnail
collection = db.users



async def set_thumbnail(user_id, file_id):
    await collection.update_one({'_id': int(user_id)}, {'$set': {'file_id': file_id}})

async def get_thumbnail(user_id):
    user = await collection.find_one({'_id': int(user_id)})
    return user.get('file_id', None)

