# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)
# By Joshua & Joe (dad) Gardner :)

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

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 12
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)

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
        neopixels[pixel] = pcolor
        neopixels.show()
        pixel=(pixel + 1)
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
        for game in range(1,13):
            print("This is the beginning of game ",game," the score is ",scores)
            #displayscore()
            clearring()
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
                        break
                        button2wait()
                        button2hold()
                #print("Delay Count is ",delaycount," currentdelaycount is ", currentdelaycount)
                delaycount = currentdelaycount
                lastchasepixel = chasepixel % NUMPIXELS
                chasepixel = (chasepixel + 1) % NUMPIXELS
                if mode == "clock":
                    break
                #time.sleep(delay)  # make bigger to slow down
            if mode == "clock":
                    break
            clearring()
            displayscore()
            buttonwait() #This holds the score on the screen until the button is pressed instead of having to wait some number of seconds
            buttonhold() #This prevents an early button read after clearing the score
    scores.clear()
    while mode=="clock":
        print("This is the clock mode and will sit here until we put more in here")
        clearring()
        buttonwait()
        buttonhold()
        mode="game"