#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from os import listdir, linesep
from subprocess import Popen, PIPE
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

    async def url_downloader(self, event, process_msg, bot, url):
        task("Running")

        len_file = await length_of_file(url)
        if len_file == 'Valid':
            msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
            userid = event.sender_id
            files_before = listdir()

            #Downloading File From Url
            process = Popen(['wget', url], stderr=PIPE)
            started = False
            for line in process.stderr:
                line = line.decode("utf-8", "replace")
                print(line)
                if started:
                    splited = line.split()
                    if len(splited) == 9:
                        completed = splited[0]
                        if completed.endswith('K'):
                            completed = str(round(int(completed[:len(completed)-1])/1024, 2))+'M'
                        percentage = splited[6]
                        speed = splited[7]
                        remaining = splited[8]
                        msg = await bot.edit_message(msg, f"<b>Downloading... !! Keep patience...\n📊Percentage: {percentage}\n✅Completed: {completed+'B'}\n🚀Speed: {speed}B/s\n⌚️Remaining Time: {remaining}</b>", parse_mode = 'html')
                elif line == linesep:
                    started = True
            else:
                files_after = listdir()
                try:
                    filename = str([i for i in files_after if i not in files_before][0])
                except IndexError:  #When File Not Downloaded
                    task("No Task")
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, unsuccessful_upload, parse_mode = 'html')
                else:
                    n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True
        elif len_file == 'Not Valid':
            await bot.edit_message(process_msg, unsuccessful_upload, parse_mode = 'html')
        else:
            await bot.edit_message(process_msg, f'This filesize is **{len_file}mb**. {file_limit}', parse_mode = 'html')
        self.filename = None
        task("No Task")
        return None