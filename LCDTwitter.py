from twython import Twython
from pprint import pprint
import time
import threading
import sys
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class TwitterLCD(Adafruit_CharLCDPlate, threading.Thread):
    def __init__(self, twitter):
        Adafruit_CharLCDPlate.__init__(self)
        threading.Thread.__init__(self)
        self.twitter = twitter
        self.query = None
        self.col = (lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL,
                lcd.BLUE, lcd.VIOLET, lcd.ON)
        self.paused = False
        
    def run(self):
        self.LoopTweets()
    
    def Timeline(self):
        self.query = self.twitter.get_home_timeline()

    def WrapMessage(self, text):
        if 33 > len(text) > 16:
            toList = list(text)
            self.message(''.join(toList[0:16]) + "\n" + ''.join(toList[16:]))
            time.sleep(2)
        elif len(text) < 16:
            self.message(text)
        if len(text) > 32:
            messageToPrint = list(text)
            while len(messageToPrint) > 32:
            
                lcdMessage = ''.join(messageToPrint[0:16])
                SecondLine = ''.join(messageToPrint[16:32])
                messageToPrint = messageToPrint[32:]
                self.message(lcdMessage + "\n" + SecondLine)
                time.sleep(2)
                self.clear()
            if len(messageToPrint) > 0:
                if len(messageToPrint) > 16:
                    self.message(''.join(messageToPrint[:16]) + "\n" + ''.join(messageToPrint[16:]))

                else:
                    self.message(''.join(messageToPrint))

    def LoopTweets(self):
        global semaphore
        while True:
            semaphore.acquire()
            for item, colour in zip(self.query, self.col):
                self.clear()
                self.backlight(colour)
                screen = item['user']['screen_name']
                name = item['user']['name']
                tweet = item['text']
                try:
                    print tweet
                except UnicodeEncodeError:
                    print "skipping tweet..."
                    continue
    
                date = item['created_at']
                try:
                    print name + " @" + screen
                except UnicodeEncodeError:
                    print "skipping tweet..."
                    continue
                self.WrapMessage(name + " @" + screen)
                time.sleep(2)
                self.clear()
                self.WrapMessage(tweet)
        if event.is_set():
            self.clear()
            self.message("HI CHARLOTTE!")
            time.sleep(10)

    def PollButton(self, btn, event):
        global semaphore
        while True:
            if self.buttonPressed(btn):
                print "clicked"
                semaphore.acquire()
                semaphore.release()
APP_KEY = 'Bnjesgy6vEoEJ10lJPJixQ'
APP_SECRET = '9LajtmzT42dcgWmoU7LBibSc5n2orToiH6ObDSYCE'

OAUTH_TOKEN = '28185894-d4Ax4xiD2IqopvaCKSGdsqmKVQtr4i8mZK6YOhjI'
OAUTH_TOKEN_SECRET = 'zDHr6TKDzviyn2uCIVjXbZsvojxNAeNFPjrivIpPo'
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
lcd = Adafruit_CharLCDPlate()
semaphore = threading.Semaphore()
event = threading.Event()
NewProj = TwitterLCD(twitter)

Selected= threading.Thread(group=None, target=NewProj.PollButton, name=None, args=(NewProj.SELECT,event), kwargs={})
NewProj.Timeline()
NewProj.start()
Selected.start()
