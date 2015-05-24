from twython import Twython
from pprint import pprint
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
twitter = Twython()
APP_KEY = ''
APP_SECRET = ''

OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_home_timeline()
lcd = Adafruit_CharLCDPlate()
col = (lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON)
paused = False

current = {'tweet': None,
            'date': None,
            'screen': None,
            'name': None }

btn = {'left': lcd.LEFT,
        'up': lcd.UP,
        'down': lcd.DOWN,
        'right': lcd.RIGHT,
       'select': lcd.SELECT}
def WrapText(text):
    if 33 > len(text) < 16:
            toList = list(text)
            lcd.message(''.join(toList[0:16]))
            lcd.message(''.join(toList[16:]))
            time.sleep(2)
    else:
        lcd.message(text)
    if len(text) > 32:
        messageToPrint = list(text)
        while len(messageToPrint) > 32:
            lcdMessage = ''.join(messageToPrint[0:16])
            SecondLine = ''.join(messageToPrint[16:32])
            messageToPrint = messageToPrint[32:]
            lcd.message(lcdMessage + "\n" + SecondLine)
            time.sleep(2)
            lcd.clear()
        if len(messageToPrint) > 0:
            if len(messageToPrint) > 16:
                lcd.message(''.join(messageToPrint[:16]))
                lcd.message(''.join(messageToPrint[16:]))

            else:
                lcd.message(''.join(messageToPrint))
       
       
def LoopTweets():
    for item, colour in zip(timeline, col):
        lcd.clear()
        lcd.backlight(colour)
        screen = item['user']['screen_name']
        current["screen"] = screen
        name = item['user']['name']
        current["name"] = name
        tweet = item['text']
        current["tweet"] = tweet
        try:
            print tweet
        except UnicodeEncodeError:
            print "skipping tweet..."
            continue
        date = item['created_at']
        current["date"] = date
        message = name + " @" + screen
        WrapText(message)
        time.sleep(2)
        lcd.clear()
        WrapText(tweet)
        time.sleep(3)
        if lcd.buttonPressed(btn['select']) and paused==False:
            print "hello"
            paused=True
            break

while True:
    if paused==False:
        LoopTweets()
    else:
        # loop through the current tweet and it's info until select is pressed again
        while paused:
            WrapText(current["name"] + " @" + current["screen"])
            time.sleep(3)
            WrapText(current["tweet"])
            time.sleep(3)
        if lcd.buttonPressed(btn['select']):
            paused=False
            break
            
    if lcd.buttonPressed(btn['select']) and paused==False:
        paused=True
    elif lcd.buttonPressed(btn['select']) and paused==True:
        paused=False
