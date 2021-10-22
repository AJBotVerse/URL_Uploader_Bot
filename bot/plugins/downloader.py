#!/usr/bin/env python3



"""Importing"""
# Importing External Packages
from pySmartDL import SmartDL

# Importing Inbuilt Packages
from time import sleep
from os import remove
from re import match

# Importing Developer defined modules & data
from bot.messages import *
from bot.plugins.funcs import *


class Downloader:

    def __init__(self, event, url, bot):
        self.event = event
        self.url = url
        self.bot = bot
    
    @classmethod
    async def start(cls, event, url, bot):
        self = cls(event, url, bot)
        if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):
            await event.respond(youtube_url, parse_mode = 'html')
        else:   #Normal Url
            process_msg = await event.respond(processing_url, parse_mode = 'html')
            await self.url_downloader(self.event, process_msg, self.bot, self.url)
        return self

    async def url_downloader(self, event, process_msg, bot, url):
        task("Running")

        len_file = await length_of_file(url)
        if len_file == 'Valid':
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
            userid = event.sender_id

            downObj = SmartDL(self.url, dest = downloadFolder)
            downObj.start(blocking = False)
            while not downObj.isFinished():
                progress_bar = downObj.get_progress_bar().replace('#', '■').replace('-', '□')
                completed = downObj.get_dl_size(human=True)
                speed = downObj.get_speed(human=True)
                remaining = downObj.get_eta(human=True)
                percentage = int(downObj.get_progress()*100)
                msg = await self.bot.edit_message(msg, f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}\n✅Completed: {completed}\n🚀Speed: {speed}\n⌚️Remaining Time: {remaining}</b>", parse_mode = 'html')
                sleep(1)
            try:
                filename = downObj.get_dest()
            except Exception as e:
                await self.bot.send_message(dev, f'In urlDL.py {line_number()} {e}')
            if downObj.isSuccessful():
                n_msg = await self.bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                self.n_msg, self.filename = n_msg, filename
                return True
            else:
                task("No Task")
                try:
                    remove(f'{downloadFolder}{filename}')
                except Exception as e:
                    await self.bot.send_message(dev, f'In urlDL.py {line_number()} {e}')
                    await self.bot.delete_messages(None, msg)
                    await self.bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                    for e in downObj.get_errors():
                        await self.bot.send_message(dev, f'In urlDL.py {line_number()} {str(e)}')
        elif len_file == 'Not Valid':
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
        self.filename = None
        task("No Task")
        return None