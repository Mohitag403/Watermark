import datetime
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.watermark
db = db.watermark_db




async def get_data(user_id):
    x = await db.find_one({"_id": user_id})
    return x
    
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


async def set_watermark(user_id, watermark_image):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"watermark_image": watermark_image}})
    else:
        await db.insert_one({"_id": user_id, "watermark_image": watermark_image})


async def set_watermark_text(user_id, watermark_text):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"watermark_text": watermark_text}})
    else:
        await db.insert_one({"_id": user_id, "watermark_text": watermark_text})


async def remove_thumbnail(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"thumb": None}})

async def remove_caption(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"caption": None}})

async def remove_watermark(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"watermark_image": None}})

async def remove_watermark_text(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"watermark_text": None}})

