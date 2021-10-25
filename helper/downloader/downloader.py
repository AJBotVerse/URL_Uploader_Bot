#!/usr/bin/env python3


"""Importing"""
# Importing Inbuilt Packages
from re import match

# Importing Developer defined Module
from helper.downloader.urlDL import *


class Downloader:

    def __init__(self, update, url, bot):
        self.update = update
        self.url = url
        self.bot = bot
    
    @classmethod
    async def start(cls, update, url, bot):
        self = cls(update, url, bot)
        if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):
            await update.reply_text(BotMessage.youtube_url, parse_mode = 'html')
        else:   #Normal Url
            process_msg = await update.reply_text(BotMessage.processing_url, parse_mode = 'html')
            urldownOBJ = URLDL(update, process_msg, bot, url)
            await urldownOBJ.start()
            if urldownOBJ.filename:
                self.n_msg = urldownOBJ.n_msg
            self.filename = urldownOBJ.filename
        return self

