from pyrogram import filters
from pyrogram.types import Message
from Downloader import app
from Downloader.core.database import get_sudoers, add_sudo, remove_sudo, extract_user, SUDOERS
import config
from config import OWNER_ID

@app.on_message(filters.command(["addsudo"]))
async def useradd(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.")
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(f"» {0} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.".format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"» ᴀᴅᴅᴇᴅ {0} ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.".format(user.mention))
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ.")


@app.on_message(filters.command(["delsudo", "rmsudo"]))
async def userdel(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.")
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text("» {0} ɪs ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.".format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text("» ʀᴇᴍᴏᴠᴇᴅ {0} ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.".format(user.mention))
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ.")


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]))
async def sudoers_list(client, message: Message):
#    sudoers = await get_sudoers()
#    if sudoers:
#        sudoer_list = "\n".join(str(user_id) for user_id in sudoers)
#        await message.reply_text(f"Sudoers:\n{sudoer_list}")
#    else:
#        await message.reply_text("No sudoers found.")
    text = "<u><b>🥀 ᴏᴡɴᴇʀ :</b></u>\n"
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    text += f"1➤ {user}\n"
    count = 0
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
            except:
                continue
    if not text:
        await message.reply_text("» ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ.")
    else:
        await message.reply_text(text, reply_markup=close_markup(_))
