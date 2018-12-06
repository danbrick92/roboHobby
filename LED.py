import sys
import RPi.GPIO as GPIO

# Check for pin #

if sys.argv[1].lower() != 'on' and sys.argv[1].lower() != 'off':
    print("Must provide on or off") 
    exit(1)
if sys.argv[2] == "":
    print("Must provide pin # to light up") 
    exit(1)
    
state = sys.argv[1]    
ledPin = int(sys.argv[2])

GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location 
GPIO.setup(ledPin, GPIO.OUT) # Set ledPin to output mode
if state == 'on':
    GPIO.output(ledPin, GPIO.HIGH)
else:
    GPIO.output(ledPin, GPIO.LOW)