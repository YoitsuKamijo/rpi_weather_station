import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

GPIO.output(21, False) 
time.sleep(0.5)
GPIO.output(21, True)
time.sleep(0.5)
GPIO.output(21, False)
time.sleep(0.25)
GPIO.output(21, True)
time.sleep(0.25)
GPIO.output(21, False)
time.sleep(0.25)
GPIO.output(21, False)

