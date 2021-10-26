#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from helper.importCommon import *


#For Owner of Bot Only, Sent message to all Bot Users
@Client.on_message(filters.chat(Config.OWNER_ID) & filters.regex("^/add(.+)"))
async def broadcast_handler(bot, update):
    try:
        #Extracting userid
        userid = str(update.text.split('/add ')[1])
    except IndexError:
        await update.reply_text(BotMessage.addcommandinvaild, parse_mode = 'html')
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    else:
        if userid.isdigit():
            if addingPremiumUser(userid):
                await update.reply_text(BotMessage.successfullyadded, parse_mode = 'html')
            else:
                await update.reply_text(BotMessage.addingWentWrong, parse_mode = 'html')
        else:
            await update.reply_text(BotMessage.addcommandinvaild, parse_mode = 'html')

