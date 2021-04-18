import RPi.GPIO as GPIO
import time

relayOne_pin = 26 # IN1 GPIO PIN
#relayTwo_pin = 19 # IN2 GPIO PIN

relayOne_LED = 20 # IN1 GPIO PIN
#relayTwo_LED = 21 # IN2 GPIO PIN

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(relayOne_pin, GPIO.OUT)
#GPIO.setup(relayTwo_pin, GPIO.OUT)
GPIO.setup(relayOne_LED, GPIO.OUT)
#GPIO.setup(relayTwo_LED, GPIO.OUT)

GPIO.output(relayOne_pin, 1)
#GPIO.output(relayTwo_pin, 1)
GPIO.output(relayOne_LED, 1)
#GPIO.output(relayTwo_LED, 1)

def LedVisualDeterrent(Switch):
    
    if Switch == 0:
        
        print ("LED on")
        print (" ")
        GPIO.output(relayOne_pin, 0)
        #GPIO.output(relayTwo_pin, 0)
        
    elif Switch == 1:
        
        print ("LED off")
        print (" ")
        GPIO.output(relayOne_pin, 1)
        #GPIO.output(relayTwo_pin, 1)
        
    else:
        
        print ("LedVisualDeterrent only accepts '0'=ON or '1'=OFF")
 

LedVisualDeterrent(0)
time.sleep(3)
LedVisualDeterrent(1) 

