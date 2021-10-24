#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram.errors import exceptions

# Importing Common Files
from helper.importCommon import *


# Current Filename
fileName = 'broadcast'


#For Owner of Bot Only, Sent message to all Bot Users
@Client.on_message(filters.chat(Config.OWNER_ID) & filters.regex("^/broadcast(.+)"))
async def broadcast_handler(bot, update):
    try:
        #Extracting Broadcasting Message
        message = update.text.split('/broadcast ')[1]
    except IndexError:
        await update.reply_text(BotMessage.broadcast_failed, parse_mode = 'html')
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    else:
        #Getting User`s Id from Database
        for userid in [document['userid'] for document in collection_user.find()]:
            try:
                #Sending Message One By One
                await bot.send_message(userid, message)
            except exceptions.bad_request_400.UserIsBlocked:
                #User Blocked the bot
                collection_user.delete_one({'userid' : userid})
            except Exception as e:
                await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    return

