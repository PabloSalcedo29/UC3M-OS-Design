import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

for i in range(10):
    print("ON: ", i+1)
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1)
    print("OFF: ", i+1)
    GPIO.output(18, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()