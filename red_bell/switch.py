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

def get_state(pin):
    try:
        state = GPIO.input(pin)
    except:
        GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location 
        GPIO.setup(pin, GPIO.OUT)
        state = GPIO.input(pin)
    #print("Pin {} is {}".format(pin,state))
    return state
    
def check_if_on():
    state = get_state(29)
    if state == True:
        state = get_state(31)
        print("Device is {}".format(state))
    else:
        switch_pin(29)
        check_if_on()
    return state