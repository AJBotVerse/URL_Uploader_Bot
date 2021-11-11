#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from requests import get
from bs4 import BeautifulSoup

# Importing Inbuilt Packages
from re import match
from json import loads

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
        self.process_msg = await update.reply_text(BotMessage.processing_url, parse_mode = 'html')
        if match('^(https://)?(www.)?youtu(.)?be(.com)?/(.*)', url):
            await update.reply_text(BotMessage.youtube_url, parse_mode = 'html')
        elif match('^(http(s)?://)?(www.)?(cofilink.com|pdisk1.net|pdisk.net|pdisks.com)/share-video\?videoid=(.*)', url):
            await self.pdiskRawLinkExtract()
        else:   #Normal Url
            await self.rawLinkDownloader()
        return self

    async def rawLinkDownloader(self, customFileName = None):
        urldownOBJ = URLDL(self.update, self.process_msg, self.bot, self.url, customFileName)
        await urldownOBJ.start()
        if urldownOBJ.filename:
            self.n_msg = urldownOBJ.n_msg
        self.filename = urldownOBJ.filename
        self.downloadFolder = urldownOBJ.Downloadfolder
    
    async def pdiskRawLinkExtract(self):
        res = get(self.url)
        page = BeautifulSoup(res.content, 'html5lib')
        try:
            scriptValue = str(page.find_all('script')[2]).split('<script> window.__INITIAL_STATE__= ')[1].split(';</script>')[0]
            jsonDoc = loads(scriptValue)
            self.url = jsonDoc['infoData']['defaultUrl']
        except Exception as e:
            await self.bot.send_message(Config.OWNER_ID, f'{line_number(fileName, e)}\n\n{self.url}')
            await self.bot.edit_message_text(self.userid, self.process_msg.message_id, BotMessage.unsuccessful_upload, parse_mode = 'html')
            return
        else:
            try:
                customFileName = str(page.find('p', {"class" : 'title text-ellipsis'}).contents[0])
            except Exception as e:
                customFileName = None
            else:
                customFileName += '.mp4'
            finally:
                await self.rawLinkDownloader(customFileName)
        
        