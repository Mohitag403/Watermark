import motor.motor_asyncio
from config import MONGO_DB

_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
db = _client["watermark"]
col = db.user



def new_user(id):
    return dict(
        _id=int(id),                                   
        file_id=None,
        caption=None
    )

async def add_user(id):
    user = new_user(id)
    await col.insert_one(user)

async def is_user_exist(id):
    user = await col.find_one({'_id': int(id)})
    return bool(user)

async def total_users_count():
    count = await col.count_documents({})
    return count

async def get_all_users():
    all_users = col.find({})
    return all_users

async def delete_user(user_id):
    await col.delete_many({'_id': int(user_id)})

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



