#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram.errors import exceptions

# Importing Common Files
from helper.importCommon import *

# Importing Inbuilt Packages
from shutil import rmtree
from time import time, sleep


class Upload:

    def __init__(self, bot, update, old_msg, filename, downloadFolder):
        self.bot = bot
        self.userid = update.chat.id
        self.msg_id = update.message_id
        self.old_msg = old_msg
        self.filename = filename
        self.downloadFolder = downloadFolder

    async def start(self):
        fileName = 'uploader.py'

        async def editMessage(progress_bar, percentage, completed, speed, remaining):
            try:
                self.old_msg = await self.bot.edit_message_text(self.userid, self.old_msg.message_id, f"<b>Now Uploading... !! Have patience... ⌛\n [{progress_bar}]\n📊Percentage: {percentage} %\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
            except exceptions.bad_request_400.MessageNotModified:
                pass

        def uploadingProgress(current, total):
            percentFraction = current/total
            progress = int(18*percentFraction)
            progress_bar = '■' * progress + '□' * (18 - progress)
            percentage = int((percentFraction)*100)
            currentMB = (current/1024)/1024
            completed = int(currentMB)
            speed = round(currentMB/(time() - t1), 2)
            if not speed:
                speed = 0.01
            remaining = int((((total - current)/1024)/1024)/speed)
            print(f"{current} {total} [{progress_bar}] {percentage} % {completed} MB {speed} MB/s {remaining} seconds")
            self.bot.loop.create_task(editMessage(progress_bar, percentage, completed, speed, remaining))
            sleep(3)

        try:
            global t1
            t1 = time()
            # await self.bot.send_document(self.userid , document = self.filename, reply_to_message_id = self.msg_id, progress = uploadingProgress)
            await self.bot.send_document(self.userid , document = self.filename, reply_to_message_id = self.msg_id)
        except Exception as e:
            await self.bot.delete_messages(self.userid, self.old_msg.message_id)
            await self.bot.send_message(self.userid, BotMessage.unsuccessful_upload, reply_to_message_id  = self.msg_id)
            await self.bot.send_message(Config.OWNER_ID, line_number(fileName, e))
        else:
            await self.bot.delete_messages(self.userid, self.old_msg.message_id)
        finally:
            rmtree(self.downloadFolder)

