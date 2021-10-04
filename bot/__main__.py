#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from telethon import events
from telethon.sync import TelegramClient
from os import remove
from bot.plugins.downloader import *
from bot.messages import *


'''Login as a Bot'''
bot = TelegramClient('URL_Uploader', api_id, api_hash).start(bot_token = bot_token)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    await event.respond(start_msg, parse_mode = 'html')

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    await event.respond(help_msg, parse_mode = 'html')

@bot.on(events.NewMessage)
async def upload_handler(event):

    message_info = event.message

    if str(type(message_info.entities[0])) == "<class 'telethon.tl.types.MessageEntityUrl'>":
        if task() == "Running":
            await event.respond(task_ongoing, parse_mode = 'html')
        else:
            url = message_info.text
            downloader = await Downloader.start(event, url, bot)
            filename = downloader.filename

            if filename:    #Sending file to user
                msg = downloader.n_msg
                message = event.message
                userid = event.sender_id
                try:
                    await bot.send_file(userid , file = filename, reply_to = message)
                except Exception as e:
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, unsuccessful_upload, reply_to = message)
                    print(line_number(), e)
                else:
                    await bot.delete_messages(None, msg)
                finally:
                    remove(filename)
            task("No Task")
    return None


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()