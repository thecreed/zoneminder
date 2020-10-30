#!/usr/bin/python3

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
from subprocess import Popen,DEVNULL

# https://realpython.com/python-logging/
import sys
sys.path.append("/root/watchdog/")
from watchdog_logging import *

import telegram
from load_config import config


class MyHandler(FileSystemEventHandler):
    def __init__(
        self,
        logger,
        telegram,
    ):
        self.AlreadySended = []
        self.logger = logger
        self.telegram = telegram
    
    def on_modified(self, event):
        self.logger.error(f"File modified: {event.src_path}")
    
    def on_created(self, event):
        self.logger.error(f"File created: {event.src_path}")
        if '.mp4' in event.src_path and \
                not event.src_path in self.AlreadySended: # This avoid send file than once.
            
            # Waits until the zm finish the generation of the file.
            while True:
                if Popen(['/usr/bin/lsof', event.src_path], stdout=DEVNULL, stderr=DEVNULL).wait() == 0:
                    time.sleep(2)
                    self.logger.error(f'File {event.src_path} is still opened')
                    continue
                else:
                    break
            
            self.logger.error(f'File {event.src_path} copy has now finished')
            
            # Send telegram message about the event
            #Text = f'event type: {event.event_type}  path : {event.src_path}'
            #self.telegram.send_message(Tex)
            
            # Send the file via telegram
            self.logger.error(f'Sending file via telegram. Group: {self.telegram.TelegramChatID}')
            Time = datetime.datetime.now()
            FileName='Video_'+str(Time.day)+"-"+str(Time.month)+\
                    "-"+str(Time.year)+"_"+str(Time.hour)+"-"+\
                    str(Time.minute)+"-"+str(Time.second)+".mp4"
            
            # Send file to telegram
            attempts=0
            while attempts < 10:
                try:
                    self.telegram.send_video(FileName, event.src_path)
                    self.logger.error('File sended')
                    self.AlreadySended.append(event.src_path)
                    break
                except:
                    attempts += 1
                    self.logger.error('Error trying send file.')
    
    def on_deleted(self, event):
        self.logger.error(f"File deleted: {event.src_path}")
    
    def on_moved(self, event):
        self.logger.error(f"File moved: {event.src_path} to {event.dest_path}")

path = '/var/cache/zoneminder/events/1'

if __name__ == "__main__":
    tg = telegram.telegram(
            #TelegramToken = "986337068:AAHWsVbzhJ4YvVANEtbwtr8ULAb73A9bgdg",
            TelegramToken = config.telegram_token,
            #TelegramChatID = '-1001378133873'
            TelegramChatID = config.telegram_chat_id 
            )
    event_handler = MyHandler(
            logger = logger,
            telegram = tg)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



