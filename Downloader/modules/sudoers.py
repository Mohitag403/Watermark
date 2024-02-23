import random
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from pyrogram.types import Message, User
from config import OWNER_ID, MONGO_DB_URI
from pyrogram import Client
from Downloader import app

mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
mongodb = mongo_client.TXT
sudoersdb = mongodb.sudoers

async def get_sudoers() -> List[int]:
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

async def extract_user(m: Message) -> User:
    try:
        if m.reply_to_message:
            return m.reply_to_message.from_user
        elif m.entities:
            msg_entities = m.entities[1] if m.text.startswith("/") else m.entities[0]
            user_id = msg_entities.user.id if msg_entities.type == "text_mention" else int(
                m.command[1]) if m.command[1].isdecimal() else m.command[1]
            return await app.get_users(user_id)
        else:
            return None
    except Exception as e:
        print(f"Error extracting user: {str(e)}")
        return None


@app.on_message(filters.command(["addsudo"]))
async def useradd(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Invalid usage. Use /addsudo [user]")
    user = await extract_user(message)
    if user:
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("User is already a sudoer.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(f"Added {user.first_name} as a sudoer.")
        else:
            await message.reply_text("Failed to add user as a sudoer.")
    else:
        await message.reply_text("User not found.")

@app.on_message(filters.command(["delsudo", "rmsudo"]))
async def userdel(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Invalid usage. Use /delsudo [user]")
    user = await extract_user(message)
    if user:
        sudoers = await get_sudoers()
        if user.id not in sudoers:
            return await message.reply_text("User is not a sudoer.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"Removed {user.first_name} from sudoers.")
        else:
            await message.reply_text("Failed to remove user from sudoers.")
    else:
        await message.reply_text("User not found.")

@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]))
async def sudoers_list(client, message: Message):
    sudoers = await get_sudoers()
    if sudoers:
        sudoer_list = "\n".join(str(user_id) for user_id in sudoers)
        await message.reply_text(f"Sudoers:\n{sudoer_list}")
    else:
        await message.reply_text("No sudoers found.")
