#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from helper.importCommon import *

# Importing Developer defined Module
from helper.downloader.downloader import Downloader
from helper.uploader import *


# Current File Name
fileName = 'uploadRequest'


@Client.on_message(filters.private & filters.regex("^http?s:(.*)"))
async def upload_handler(bot, update):
    if await search_user_in_community(bot, update):
        if task() == "Running":
            await update.reply_text(BotMessage.task_ongoing, parse_mode = 'html')
        else:
            task("Running")
            url = update.text
            downloader = await Downloader.start(update, url, bot)
            filename = downloader.filename

            if filename:    #Sending file to user
                msg = downloader.n_msg
                message_id = update.message_id
                uploader = Upload(bot, update, msg, filename)
                await uploader.start()
    return