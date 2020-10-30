#!/usr/bin/python3

import requests

class telegram():
    def __init__(
        self,
        TelegramToken,
        TelegramChatID,
    ):
        self.TelegramToken = TelegramToken
        self.TelegramChatID = TelegramChatID
    def send_message(self, text):
        files = {
            'chat_id': (None, self.TelegramChatID),
            'text': text,
        }
        response = requests.get("https://api.telegram.org/bot"+self.TelegramToken+"/sendMessage?chat_id="+self.TelegramChatID+"&text="+text, files=files)
        return response
    
    def send_file(self, FileName, FilePath):
        files = {
            'chat_id': (None, self.TelegramChatID),
            'document': (FileName, open(FilePath, 'rb')),
        }
        response = requests.post("https://api.telegram.org/bot"+self.TelegramToken+"/sendDocument", files=files)
        return response
    
    def send_video(self, FileName, FilePath):
        files = {
            'chat_id': (None, self.TelegramChatID),
            'video': (FileName, open(FilePath, 'rb')),
        }
        response = requests.post("https://api.telegram.org/bot"+self.TelegramToken+"/sendVideo", files=files)
        return response


