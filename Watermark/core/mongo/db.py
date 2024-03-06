import datetime
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.watermark
db = db.watermark_db


async def bot_on_off(x, y):
    data = await get_thumbnail(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": x}, {"$set": {"Bot": y}})
    else:
        await db.insert_one({"_id": x, "Bot": y})



async def set_thumbnail(user_id, thumb):
    data = await get_thumbnail(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"thumb": thumb}})
    else:
        await db.insert_one({"_id": user_id, "thumb": thumb})

async def get_thumbnail(user_id):
    x = await db.find_one({"_id": user_id})
    return x



async def set_caption(user_id, caption):
    data = await get_thumbnail(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"caption": caption}})
    else:
        await db.insert_one({"_id": user_id, "caption": caption})

async def get_caption(user_id):
    x = await db.find_one({"_id": user_id})
    return x
    


async def set_watermarl(user_id, watermark):
    data = await get_thumbnail(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"watermark": watermark}})
    else:
        await db.insert_one({"_id": user_id, "watermark": watermark})

async def get_watermark(user_id):
    x = await db.find_one({"_id": user_id})
    return x



async def remove_thumbnail(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"thumb": None}})

async def remove_caption(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"caption": None}})

async def remove_watermark(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"watermark": None}})


