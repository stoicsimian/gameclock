# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)
# Games and Clock By Joshua & Joe (dad) Gardner :)

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import adafruit_dotstar as dotstar
import time
import neopixel

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.05)

# Digital input with pullup on D2
button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Digital input with pullup on D4
button2 = DigitalInOut(board.D0)
button2.direction = Direction.INPUT
button2.pull = Pull.UP

# NeoPixel rings (of 12 and 24 LEDs) connected on D4
NUMPIXELS = 36
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.05, auto_write=False)

ring1 = 12
ring2 = 24

######################### SOME HELPFUL VALUES ####################
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0, 0, 0)

# How many cycles will the color sit on a single color
basepixel = 0
basecolor = GREEN
chasepixel = 6
chasecolor = RED
lastchasepixel = 5
bothcolor = PURPLE
#startdelay = 0.02
#delay = startdelay
startdelaycount = 200
delaycount = startdelaycount
currentdelaycount = startdelaycount
numgames = 12 # how many games to play before resetting the score
scores=[] # the empty array to hold the scores
scorecolors = {200: GREEN,
               400: BLUE,
               800: YELLOW,
               1600: PURPLE,
               3200: RED}
nextgame=1
mode="game"

######################### HELPERS ########################
def clearring():
    for p in range(NUMPIXELS):
        neopixels[p] = (0, 0, 0)
    neopixels.show()

def clearring1():
    for p in range(ring1):
        neopixels[p] = (0, 0, 0)
    neopixels.show()

def setstart():
    neopixels[basepixel] = basecolor # Set Pixel 0 to green as a starting place
    neopixels.show()
    neopixels[chasepixel] = chasecolor # Set pixel 6 to red as a starting place
    neopixels.show()

def displayscore():
    pixel=0
    for p in scores:
        if p > 3200:
            pcolor=RED
        else:
            pcolor=scorecolors[p]
        scorepixel = pixel + (ring1 )
        neopixels[scorepixel] = pcolor
        pixel=(pixel + 1)
    neopixels.show()
    #time.sleep(5)  

def drawgame():
    if chasepixel == basepixel:
        neopixels[basepixel] = bothcolor
        neopixels[lastchasepixel] = OFF
        neopixels.show()
        #print("Delay Count is ",delaycount," currentdelaycount is ", currentdelaycount,"Game is ",game," and score is ", scores)
    elif lastchasepixel == basepixel:
        neopixels[basepixel] = basecolor
        neopixels[chasepixel] = chasecolor
        neopixels.show()
    else:
        # print("Time to set the other stuff")
        neopixels[chasepixel] = chasecolor
        # neopixels.show()
        neopixels[lastchasepixel] = OFF
        neopixels.show()

def buttonhold():
    while not button.value: # This loop holds the progam in place while the button is pressed,
    # print("The Button is still pressed")
        pass # Using pass here because we don't need to do anything but need something in the while loop

def buttonwait():
    while button.value: # This loop holds the progam in place while the button is pressed,
    # print("The Button is still pressed")
        pass # Using pass here because we don't need to do anything but need something in the while loop

def button2hold():
    while not button2.value: # This loop holds the progam in place while the button is pressed,
    # print("The Button is still pressed")
        pass # Using pass here because we don't need to do anything but need something in the while loop

def button2wait():
    while button2.value: # This loop holds the progam in place while the button is pressed,
    # print("The Button is still pressed")
        pass # Using pass here because we don't need to do anything but need something in the while loop

######################### SET START STATE ########################

# turn off the LED on the board
dot[0] = (0, 0, 0)

clearring()
time.sleep(1) # Give us a 1 second wait until we start

setstart()
time.sleep(1) # Give us a 1 second wait until we really get going

######################### MAIN LOOP ##############################

while True:
    while mode=="game":
        for game in range(1,25):
            print("This is the beginning of game ",game," the score is ",scores)
            #displayscore()
            clearring1()
            setstart()
            nextgame=1
            while nextgame > 0:
                # Set the necessary pixels to the right colors
                #print("Chasepixel is ", chasepixel, " and Lastpixel is ", lastchasepixel)
                #print("Game is ",game," and nextgame is ",nextgame)
                drawgame()
                while delaycount > 0:
                    if not button.value:
                        print("Button Pressed!")
                        if chasepixel == basepixel:
                            print("You did it !!!  Resetting the delay to ", startdelaycount)
                            print("Adding the current delay count ",currentdelaycount,"to the score of",scores)
                            scores.append(currentdelaycount)
                            currentdelaycount = startdelaycount
                            nextgame=0
                            delaycount=0
                            print("Value of nextgame is ,",nextgame)
                        else:
                            print(
                                "You missed, slowing it down for you. Delay of ",
                                delaycount,
                                " will be doubled.",
                            )
                            currentdelaycount = currentdelaycount * 2
                            delaycount = currentdelaycount
                            print("Delaycount is now ", delaycount)
                        # Hold the loop here until the button is no longer pressed
                        buttonhold()
                    delaycount = (delaycount - 1)
                    if not button2.value:
                        print("Button 2 has been pressed")
                        mode="clock"
                        button2hold()
                        break
                #print("Delay Count is ",delaycount," currentdelaycount is ", currentdelaycount)
                delaycount = currentdelaycount
                lastchasepixel = chasepixel % ring1
                chasepixel = (chasepixel + 1) % ring1
                if mode == "clock":
                    break
                #time.sleep(delay)  # make bigger to slow down
            if mode == "clock":
                    break
            displayscore()
            buttonwait() #This holds the score on the screen until the button is pressed instead of having to wait some number of seconds
            buttonhold() #This prevents an early button read after clearing the score
        scores.clear()
        clearring()
    while mode=="clock":
        print("This is the clock mode and will sit here until we put more in here")
        clearring()
        button2wait()
        button2hold()
        mode="timer"
    while mode =="timer":
        print("This is timer mode we will count seconds on the small ring, through all colors then minutes on the big ring, up to 24.")
        clearring()
        timerstart=int(time.monotonic())
        lasttime=int(time.monotonic())
        thistime=int(time.monotonic())
        #neopixels[basepixel] = basecolor # Set Pixel 0 to green as a starting place
        #neopixels.show()
        secondspixel=0
        minutespixel=0
        timercolors = [GREEN, BLUE, YELLOW, PURPLE, RED]
        for mcolor in timercolors:
            for minutes in range(1,25):
                for scolor in timercolors:
                    print("Starting with color ",scolor)
                    while True:
                        thistime=int(time.monotonic())
                        duration=thistime - lasttime
                        #print("This Time is ",thistime,"which is ",duration,"since the Last Time, which was ",lasttime)
                        if duration == 1:
                            secondspixel = (secondspixel + 1) % ring1
                            print("The Seconds Pixel is ",secondspixel)
                            neopixels[secondspixel] = scolor
                            neopixels.show()
                            if secondspixel == 0:
                                lasttime = thistime
                                break
                        lasttime = thistime
                        if not button2.value:
                            print("Button 2 has been pressed")
                            mode="game"
                            button2hold()
                            break               
                    if mode == "game":
                        break
                if mode == "game":
                    break
                minutespixel = (minutes % ring2) + ring1
                print ("The Minutes Pixel is ",minutespixel)
                neopixels[minutespixel] = mcolor
                neopixels.show()
            if mode == "game":
                break
        if mode == "game":
            break
        print("All done with the timer waiting to see a button push")
        timerstop = int(time.monotonic())
        timerduration = timerstop - timerstart
        print("The timer ran for ",timerduration,"seconds.")