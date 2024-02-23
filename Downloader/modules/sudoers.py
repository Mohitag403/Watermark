from pyrogram import filters
from pyrogram.types import Message
from Downloader import app
from Downloader.modules.database import get_sudoers, add_sudo, remove_sudo
import config


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
