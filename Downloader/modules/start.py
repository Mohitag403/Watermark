from pyrogram import filters
from Downloader import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@app.on_message(filters.command("start"))
async def start(_,message):
  await message.reply_photo(photo="https://telegra.ph/file/9456751a4ca1a346e631f.jpg", caption="**𝙷𝚒!**\n\n**𝙶𝚒𝚟𝚎 /𝚝𝚡𝚝 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝚝𝚘 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚛𝚘𝚖 𝚊 𝚃𝚎𝚡𝚝 𝚏𝚒𝚕𝚎.**🎓✨",
                            reply_markup=InlineKeyboardMarkup([
                [
                  InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_")
                ],             
                [
                  InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/Mohitag24"),
                  InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/Mohitag24")
                ]
                            ]))



