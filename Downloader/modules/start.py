from pyrogram import filters
from Downloader import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant




async def subscribe(app, message):
   update_channel = -1001946875647
   if update_channel:
      try:
         user = await app.get_chat_member(update_channel, message.chat.id)
         if user.status == "kicked":
            await message.reply_text("Sorry Sir, You are Banned. Contact My Support Group @DevsOops")
            return 1
      except UserNotParticipant:
         await message.reply_photo(photo="https://telegra.ph/file/b7a933f423c153f866699.jpg",caption="**ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ ᴀғᴛᴇʀ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ sᴇɴᴅ /start ǫᴜᴇʀʏ**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 🤖", url=f"https://t.me/DevsOops")]]))
         return 1
      except Exception:
         await message.reply_text("Something Went Wrong. Contact My Support Group")
         return 1
        


@app.on_message(filters.command("start"))
async def start(_,message):
  join = await subscribe(_,message)
  if join ==1:
    return
  await message.reply_photo(photo="https://telegra.ph/file/9456751a4ca1a346e631f.jpg", caption="**ʜᴇʏ ᴛʜᴇʀᴇ!  ᴜɴʟᴇᴀsʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏғ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴄᴏᴜʀsᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪᴢᴀʀᴅ – ɪ'ᴍ ɴᴏᴛ Jᴜsᴛ ʏᴏᴜʀ ᴀᴠᴇʀᴀɢᴇ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ; ɪ'ᴍ ʏᴏᴜʀ ᴠɪᴘ ᴘᴀss ᴛᴏ ɢʀᴀʙʙɪɴɢ ᴏɴʟɪɴᴇ ᴄᴏᴜʀsᴇs ɪɴ sᴛʏʟᴇ!  ʀᴇᴀᴅʏ ᴛᴏ ᴇʟᴇᴠᴀᴛᴇ ʏᴏᴜʀ ʟᴇᴀʀɴɪɴɢ ɢᴀᴍᴇ? ʟᴇᴛ's ᴅɪᴠᴇ ɪɴᴛᴏ ᴛʜᴇ ᴡᴏʀʟᴅ ᴏғ ᴋɴᴏᴡʟᴇᴅɢᴇ ᴛᴏɢᴇᴛʜᴇʀ! 🎓✨**",
                            reply_markup=InlineKeyboardMarkup([
                [
                  InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_")
                ],             
                [
                  InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/DevsXCreations"),
                  InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/DevsOops")
                ]
                            ]))



