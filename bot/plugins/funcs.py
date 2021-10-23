#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from telethon import Button
from telethon.tl.functions.channels import EditCreatorRequest, GetParticipantRequest
from telethon.errors import rpcerrorlist
from pymongo import MongoClient
from requests import head

# Importing Inbuilt Packages
from inspect import currentframe
from os import path
import __main__

# Importing Developer defined modules & data
from bot.credentials import *
from bot.messages import not_joined_community


'''Connecting To Database'''
mongo_client = MongoClient(connection_string)
db_member_detail = mongo_client['AJPyroVerseMember']
collection_member = db_member_detail['memberlist']
db_user = mongo_client['URL_Uploader']
collection_user = db_user['members']


'''Defining Some Functions'''
#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(event, bot):
    try:
        await bot(GetParticipantRequest("@AJPyroVerse", event.sender_id))
        await bot(GetParticipantRequest("@AJPyroVerseGroup", event.sender_id))
    except rpcerrorlist.UserNotParticipantError:
        await event.respond(not_joined_community, parse_mode = 'html', buttons = [Button.url('Join our Channel.','https://t.me/AJPyroVerse'), Button.url('Join our Group.','https://t.me/AJPyroVerseGroup')])
        return
    except rpcerrorlist.ChatAdminRequiredError:
        return True
    except Exception as e:
        print(line_number(), e)
    else:
        return True

#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'In File {path.basename(__main__.__file__)} at line {cf.f_back.f_lineno}'

#Finding user in database, if not found then adding him
def checking_user_in_db(userid):
    if connection_string:
        document = {'userid' : userid}
        if collection_user.find_one(document):
            return True
        collection_user.insert_one(document)
    return

#it will check the length of file
async def length_of_file(url):
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
        print(e)
        return 'Not Valid'

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

