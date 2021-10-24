#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from helper.importCommon import *


"""Start Handler"""
@Client.on_message(filters.private & filters.command("start"))
async def start_handler(bot, update):
    if await search_user_in_community(bot, update):
        await update.reply_text(BotMessage.start_msg, parse_mode = 'html')
    return checking_user_in_db(update.chat.id)


"""Help Handler"""
@Client.on_message(filters.private & filters.command("help"))
async def help_handler(bot, update):
    if await search_user_in_community(bot, update):
        await update.reply_text(BotMessage.help_msg, parse_mode = 'html')
    return

