#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from telethon import events
from telethon.sync import TelegramClient

# Importing Inbuilt Packages
from os import remove

# Importing Developer defined modules & data
from bot.plugins.downloader import *
from bot.messages import *


'''Login as a Bot'''
bot = TelegramClient('URL_Uploader', api_id, api_hash).start(bot_token = bot_token)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    if event.chat_id > 0:
        if await search_user_in_community(event, bot):
            await event.respond(start_msg, parse_mode = 'html')
    return checking_user_in_db(event.sender_id)

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    if event.chat_id > 0:
        if await search_user_in_community(event, bot):
            await event.respond(help_msg, parse_mode = 'html')
    return

#For Owner Only, Sent message to all Bot Users
@bot.on(events.NewMessage(pattern = r'/broadcast'))
async def broadcast_handler(event):
    if event.chat_id > 0:
        if event.sender_id == dev:
            try:
                #Extracting Broadcasting Message
                message = str(event.message.text).split('/broadcast ')[1]
            except IndexError:
                await event.respond(broadcast_failed, parse_mode = 'html')
            except Exception as e:
                print(line_number(), e)
            else:
                #Getting User`s Id from Database
                for userid in [document['userid'] for document in collection_user.find()]:
                    try:
                        #Sending Message One By One
                        await bot.send_message(userid, message)
                    except rpcerrorlist.UserIsBlockedError:
                        #User Blocked the bot
                        collection_user.delete_one({'userid' : userid})
                    except Exception as e:
                        print(line_number(), e)
    return

@bot.on(events.NewMessage)
async def upload_handler(event):
    if event.chat_id > 0:

        message_info = event.message
        if str(type(message_info.entities[0])) == "<class 'telethon.tl.types.MessageEntityUrl'>":
            if await search_user_in_community(event, bot):
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
    return


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()