#!/usr/bin/env python3


# Importing Inbuilt Packages
import os


'''Credentials'''
dev = 1972357814

downloadFolder = '/app/download/'
# downloadFolder = 'D:\Projects\Public\MegaUploaderbot\download\\'

bot_token = os.environ["BOT_TOKEN"]

api_id = os.environ["API_ID"]

api_hash = os.environ["API_HASH"]

try:
    connection_string = os.environ["MONGO_STR"]
except KeyError:
    connection_string = None

