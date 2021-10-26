#!/usr/bin/env python3


# Bot defined Messages
class BotMessage(object):
    common_text = "\n\n<u>If you are facing any problem, so report at @AJPyroVerseGroup</u>"
    help_msg = f"<i>To use me, Just Send me any direct downloading link, and I will send you the file as telegram file.</i>{common_text}"
    start_msg = f"<b>Hi, I am URL_UploaderBot Created by @AJPyroVerse and My Developer is @AJTimePyro.</b>\n{help_msg}"
    not_joined_community = f"<b>To use this bot, you need to Join our Channel and Group.</b>{common_text}"
    broadcast_failed = "<b>Broadcasting Message can`t be empty</b>"
    processing_url = "<i>Please wait while I am Processing File</i>"
    starting_to_download = "<i>Starting to Upload the file.... Have Some Patience!!!</i>"
    unsuccessful_upload = f'Uploading went <b>Unsuccessful</b>, Something Went Wrong{common_text}'
    uploading_msg = "<b>File successfully downloaded to server, Now uploading to Drive.</b>"
    buyOurPremium = "<b>\nTo upload File more than current you have to purchase our premium subscription. To purchase it, Message @AJTimePyro</b>"
    file_limit = f"Send only those whose size is less than 400mb.{buyOurPremium}{common_text}"
    youtube_url = "<b>Currently I do not support youtube videos.</b>"
    addcommandinvaild = "<b>Send Userid also.</b>"
    successfullyadded = f"<b>User added Successfully.</b>"
    addingWentWrong = f"<b>Something went wrong user not added.</b>"
    telegramLimit = f"<b>It is more than limit of telegram.</b>"
    