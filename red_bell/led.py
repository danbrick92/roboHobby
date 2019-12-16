import RPi.GPIO as GPIO
import time

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
        print("On")
    else:
        GPIO.output(pin, GPIO.LOW)
        print("Off")
    
def hi_fast():
    switch_pin(11)
    time.sleep(.07)
    switch_pin(13)
    
def hi_slow():
    switch_pin(11)
    time.sleep(.15)
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