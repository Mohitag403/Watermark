import datetime
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.watermark
db = db.watermark_db


async def get_data():
    x = await db.find_one({"_id": "Bot"})
    return x

async def bot_on_off(y):
    data = await get_data()
    if data and data.get("_id"):
        await db.update_one({"_id": "Bot"}, {"$set": {"setup": y}})
    else:
        await db.insert_one({"_id": "Bot", "setup": y})



async def set_thumbnail(user_id, thumb):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"thumb": thumb}})
    else:
        await db.insert_one({"_id": user_id, "thumb": thumb})


async def set_caption(user_id, caption):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"caption": caption}})
    else:
        await db.insert_one({"_id": user_id, "caption": caption})


async def set_watermark(user_id, watermark):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"watermark": watermark}})
    else:
        await db.insert_one({"_id": user_id, "watermark": watermark})



async def remove_thumbnail(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"thumb": None}})

async def remove_caption(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"caption": None}})

async def remove_watermark(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"watermark": None}})


