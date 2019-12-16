import RPi.GPIO as GPIO
import time

# LED time in seconds
MED = .1
SLOW = .15
FAST = .05

def switch_pin(pin):
    """
    This function turns on or off pin depending on it's state
    """
    try:
        state = GPIO.input(pin)
    except:
        GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location 
        GPIO.setup(pin, GPIO.OUT)
        state = GPIO.input(pin)
    if state == False:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    
def hi_fade():
    switch_pin(11)
    time.sleep(FAST)
    switch_pin(13)
    
def hi_slow():
    switch_pin(11)
    time.sleep(SLOW)
    switch_pin(13)
    
def hi():
    switch_pin(11)
    switch_pin(13)  
    
def med():
    switch_pin(11)
    
def low():
    switch_pin(13)
    
def all_off():
    """
    Turns off all LEDs
    """
    GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location 
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    
def blink(on_type):
    """
    Turns a pin on and off for a standard amount of time
    """
    if on_type == 'low':
        low()
        time.sleep(FAST)
        low()
    elif on_type == 'med':
        med()
        time.sleep(FAST)
        med()
    elif on_type == 'hi':
        hi()
        time.sleep(FAST)
        hi()
    elif on_type == 'hi_slow': # takes .25 seconds
        hi_slow()
        hi_slow()
    elif on_type == 'hi_fade':
        hi_fade()
        hi_fade()
        
def get_time(on_type):
    """
    Returns the amount of time it took to turn LED on and off
    """
    if on_type == "hi_slow":
        return SLOW*2
    else:
        return FAST*2
    
#blink('hi')