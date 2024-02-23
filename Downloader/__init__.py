import asyncio, config, logging
from pyromod import listen
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from Downloder import app
from Downloader.modules.sudoers import mongodb
from Downloader.modules.sudoers import *


loop = asyncio.get_event_loop()

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

app = Client(
    ":Downloader:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def setup_sudoers():
    global SUDOERS
    SUDOERS = set()
    SUDOERS.add(config.OWNER_ID)  # Assuming config.OWNER_ID is defined elsewhere
    sudoers = await sudoers_module.get_sudoers()
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoers_module.set_sudoers(sudoers)
    for user_id in sudoers:
        SUDOERS.add(user_id)


async def info_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    await setup_sudoers()


loop.run_until_complete(info_bot())


