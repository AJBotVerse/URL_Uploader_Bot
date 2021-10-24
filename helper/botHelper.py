#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import exceptions, UserNotParticipant
from pymongo import MongoClient
from requests import head

# Importing Inbuilt Packages
import __main__
from os import path
from inspect import currentframe

# Importing Credentials & Required Data
from helper.botMessages import BotMessage
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config
finally:
    mongoSTR = Config.MONGO_STR

fileName = 'botHelper'

'''Connecting To Database'''
if mongoSTR:
    mongo_client = MongoClient(mongoSTR)
    db_user = mongo_client['Pdisk_Uploader']
    collection_user = db_user['members']

'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number(fileName, e):
    cf = currentframe()
    return f'In {fileName}.py at line {cf.f_back.f_lineno} {e}'

#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(bot, update):
    try:
        await bot.get_chat_member('@AJPyroVerse', update.chat.id)
        await bot.get_chat_member('@AJPyroVerseGroup', update.chat.id)
    except UserNotParticipant:
        await update.reply_text(BotMessage.not_joined_community, parse_mode = 'html',reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Join our Channel.',url = 'https://t.me/AJPyroVerse')],
        [InlineKeyboardButton('Join our Group.',url = 'https://t.me/AJPyroVerseGroup')]
        ]))
        return
    except exceptions.bad_request_400.ChatAdminRequired:
        return True
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
        return True
    else:
        return True

#Finding user in database, if not found then adding him
def checking_user_in_db(userid):
    if mongoSTR:
        document = {'userid' : userid}
        if collection_user.find_one(document):
            return True
        collection_user.insert_one(document)
    return

#Task Updating or Status Checking
def task(status=None):
    if status:
        with open('task.txt', 'w') as newfile:
            newfile.writelines([status])
    else:
        try:
            with open('task.txt') as file:
                return file.readlines()[0]
        except FileNotFoundError:
            return "No Task"

#it will check the length of file
async def length_of_file(bot, url):
    try:
        h = head(url, allow_redirects=True)
        header = h.headers
        content_length = int(header.get('content-length'))
        file_length = int(content_length/1048576)     #Getting Length of File
        if content_length > 419430400:  #File`s Size is more than Limit 
            return file_length
        else:   #File`s Size is in the Limit
            return 'Valid'
    except Exception as e:  #File is not Exist in Given URL
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
        return 'Not Valid'

