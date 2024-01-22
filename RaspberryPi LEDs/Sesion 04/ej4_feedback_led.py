import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN = 16
OUT =20

GPIO.setup(OUT,GPIO.OUT)
GPIO.setup(IN,GPIO.IN,pull_up_down = GPIO.PUD_UP)

try:
    while True:
        GPIO.wait_for_edge(IN,GPIO.BOTH)
        if GPIO.input(IN)==GPIO.LOW:
            GPIO.output(OUT, GPIO.HIGH)
        else:
            GPIO.output(OUT, GPIO.LOW)

finally:
    GPIO.cleanup()