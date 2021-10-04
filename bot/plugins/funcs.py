'''Impoting Libraries and Modules'''
from bot.credentials import *
from inspect import currentframe
from os import path
from requests import head
import __main__


'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'In File {path.basename(__main__.__file__)} at line {cf.f_back.f_lineno}'

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

