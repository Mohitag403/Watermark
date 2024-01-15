import os
import wget
import time
import requests
import asyncio
import datetime
import subprocess
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Downloader.core.progsbar import progress_bar
from Downloader import app
from Downloader.core import helper

class upload_tg:
    def __init__(self, app, message, name: str, file_path, path, Thumb, show_msg, caption: str) -> None:
        self.app = app
        self.message = message
        self.name = name
        self.file_path = file_path
        self.path = path
        self.thumb = Thumb
        self.temp_dir = f"{path}/{name}"
        self.show_msg = show_msg
        self.caption = caption

    async def get_thumb_duration(self):
        try:
            duration = await asyncio.to_thread(helper.get_duration, self.file_path)
        except:
            duration = int(await asyncio.to_thread(helper.duration, self.file_path))

        if self.thumb.startswith(("http://", "https://")):
            wget.download(self.thumb, f"{self.temp_dir}.jpg")
            thumbnail = f"{self.temp_dir}.jpg"
        elif os.path.isfile(self.thumb):
            thumbnail = self.thumb
        else:
            try:
                thumbnail = await asyncio.to_thread(helper.take_screen_shot, self.file_path, self.name, self.path, (duration / 2))
            except:
                subprocess.run(
                    f'ffmpeg -i "{self.file_path}" -ss 00:00:01 -vframes 1 "{self.temp_dir}.jpg"', shell=True)
                thumbnail = f"{self.temp_dir}.jpg"
        return duration, thumbnail

    async def upload_video(self):
        duration, thumbnail = await self.get_thumb_duration()
        w, h = await asyncio.to_thread(helper.get_width_height, self.file_path)
        start_time = time.time()
        try:
            await self.app.send_video(
                chat_id=self.message.chat.id,
                video=self.file_path,
                supports_streaming=True,
                caption=self.caption,
                duration=duration,
                thumb=thumbnail,
                width=w,
                height=h,
                progress=progress_bar,
                progress_args=("<b>Uploading :- </b> `{file_name}`".format(
                        file_name=f"{self.name}"), self.show_msg, start_time
                )
            )
        except Exception as e:
            await self.app.send_document(
                chat_id=self.message.chat.id,
                document=self.file_path,
                caption=self.caption,
                thumb=thumbnail,
                progress=progress_bar,
                progress_args=("<b>Uploading :- </b> `{file_name}`".format(
                        file_name=f"{self.name}"), self.show_msg, start_time
                )
            )
        os.remove(self.file_path)
        await self.show_msg.delete(True)

                
