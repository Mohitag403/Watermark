from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TXT import app
from TXT.core.database import get_sudoers, add_sudo, remove_sudo, extract_user, SUDOERS
import config
from config import OWNER_ID


@app.on_callback_query(filters.regex("^close$"))
async def close_message(_, query):
    await query.message.delete()

@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
async def useradd(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.")
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(f"» {user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.")
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"» ᴀᴅᴅᴇᴅ {user.mention} ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.")
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ.")


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def userdel(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.")
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(f"» {user.mention} ɪs ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.")
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(f"» ʀᴇᴍᴏᴠᴇᴅ {user.mention} ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.")
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ.")


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & filters.user(OWNER_ID))
async def sudoers_list(client, message: Message):
    text = "<u><b>🥀 ᴏᴡɴᴇʀ :</b></u>\n"
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    text += f"1➤ {user}\n"
    count = 1
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n<u><b>✨ sᴜᴅᴏ ᴜsᴇʀs :</b></u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception as e:
                print(f"Error: {e}")
                continue
    if count == 1:
        await message.reply_text("» ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ.")
    else:
        close_button = InlineKeyboardButton(
            text="ᴄʟᴏsᴇ",
            callback_data="close",
        )
        close_markup = InlineKeyboardMarkup([[close_button]])
        await message.reply_text(text, reply_markup=close_markup)
