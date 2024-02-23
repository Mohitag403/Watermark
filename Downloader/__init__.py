# __init__.py

import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from Downloader.modules.sudoers import setup_sudoers


async def info_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    app = Client(
        ":Downloader:",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    await setup_sudoers()


loop = asyncio.get_event_loop()
loop.run_until_complete(info_bot())
