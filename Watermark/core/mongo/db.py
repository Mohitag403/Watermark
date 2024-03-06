import motor.motor_asyncio
from config import MONGO_DB

_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
db = _client["watermark"]
col = db.user


async def set_thumbnail(id, file_id):
    await col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

async def get_thumbnail(id):
    user = await col.find_one({'_id': int(id)})
    return user.get('file_id', None)

async def set_caption(id, caption):
    await col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

async def get_caption(id):
    user = await col.find_one({'_id': int(id)})
    return user.get('caption', None)


async def set_watermark(id, watermark):
    await col.update_one({'_id': int(id)}, {'$set': {'watermark': watermark}})

async def get_thumbnail(id):
    user = await col.find_one({'_id': int(id)})
    return user.get('watermark', None)


