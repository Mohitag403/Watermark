from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_DB)
db = mongo.thumbnail
db = db.users




async def set_thumbnail(user_id, file_id):
    await db.update_one({'user_id': int(id)}, {'$set': {'file_id': file_id}})

async def get_thumbnail(user_id):
    user = await db.find_one({'user_id': int(id)})
    return user.get('file_id', None)



