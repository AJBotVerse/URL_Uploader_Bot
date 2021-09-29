#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from os import listdir, remove
from subprocess import Popen
from re import match
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

    #Downloading From url
    async def url_downloader(self, event, process_msg, bot, url):
        len_file = await length_of_file(url)
        if len_file == 'Valid':
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
            userid = event.sender_id
            try:
                files_before = listdir()

                #Downloading File From Url
                output = Popen(['wget', url])
                output.wait()
            except Exception as e:
                print(line_number(), e)
                await bot.delete_messages(None, msg)
                await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                files_after = listdir()
                try:
                    #Getting InComplete Filename
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:
                    pass
                else:
                    #Reomving Incomplete File
                    remove(filename)
                    return None
            else:
                files_after = listdir()
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:  #When File Not Downloaded
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                else:
                    #File Downloaded Successfully
                    n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True
        elif len_file == 'Not Valid':
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
        self.filename = None
        return None