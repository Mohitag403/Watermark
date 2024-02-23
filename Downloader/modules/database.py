from motor.motor_asyncio import AsyncIOMotorClient
import config
from config import MONGO_DB_URI
from pyrogram import filters


mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
mongodb = mongo_client.TXT
sudoersdb = mongodb.sudoers

SUDOERS = filters.user()


async def setup_sudoers():
    global SUDOERS
    SUDOERS = set()
    SUDOERS.add(config.OWNER_ID)  # Assuming config.OWNER_ID is defined elsewhere
    sudoers = await get_sudoers()
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await set_sudoers(sudoers)
    for user_id in sudoers:
        SUDOERS.add(user_id)


async def get_sudoers() -> list[int]:
    try:
        sudoers_doc = await sudoersdb.find_one({"sudo": "sudo"})
        if sudoers_doc:
            return sudoers_doc.get("sudoers", [])
        else:
            return []
    except Exception as e:
        print(f"Error fetching sudoers: {str(e)}")
        return []

async def add_sudo(user_id: int) -> bool:
    try:
        sudoers = await get_sudoers()
        if user_id in sudoers:
            return False  # User is already a sudoer
        sudoers.append(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
        return True
    except Exception as e:
        print(f"Error adding sudo: {str(e)}")
        return False

async def remove_sudo(user_id: int) -> bool:
    try:
        sudoers = await get_sudoers()
        if user_id not in sudoers:
            return False  # User is not a sudoer
        sudoers.remove(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
        return True
    except Exception as e:
        print(f"Error removing sudo: {str(e)}")
        return False
