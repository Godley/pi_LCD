# pi_LCD
Project to create a threaded LCD twitter scroller using raspberry pi, adafruit's LCD and python with threading to achieve it

# Usage
LCDTwitter contains the class which wraps all the functionality. I think this is an old version so the threading doesn't 100% work yet, but essentially the main thread loops the tweets coming from your account. A second thread should be started which repeatedly polls to check if a button has been pressed using method "PollButton". Give it the name of the button you want to press (SELECT LEFT RIGHT etc, they should be documented in the Adafruit LCD plate code) and a threading event. If a button is pressed it will send a signal back to the main thread.

# Keys
You do need to make sure your twitter account is set up as a developer before working with this. In the developer portal you should find all the keys once it's set up. Put these details into the variables `APP_KEY`, `APP_SECRET`, `OAUTH_TOKEN` and `OAUTH_TOKEN_SECRET` respectively. I don't remember the exact location of where you go to set up twitter developer stuff, it should be googleable.
