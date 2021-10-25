#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from helper.importCommon import *

# Importing Developer defined Module
from helper.downloader.downloader import Downloader
from helper.uploader import *


# Current File Name
fileName = 'uploadRequest'


# Some Global Variable
listTask = ['']
global counter
counter = 0


@Client.on_message(filters.private & filters.regex("^http(s)?:(.*)"))
async def upload_handler(bot, update):
    if await search_user_in_community(bot, update):
        global counter
        counter += 1
        listTask.append(Multitask(bot, update))
        bot.loop.create_task(listTask[counter].start())
    return

class Multitask:

    def __init__(self, bot, update):
        self.bot = bot
        self.update = update

    async def start(self):
        url = self.update.text
        downloader = await Downloader.start(self.update, url, self.bot)
        filename = downloader.filename

        if filename:    #Sending file to user
            msg = downloader.n_msg
            uploader = Upload(self.bot, self.update, msg, filename, downloader.downloadFolder)
            await uploader.start()

