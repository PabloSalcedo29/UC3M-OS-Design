import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN = 16
OUT =20

GPIO.setup(OUT,GPIO.OUT)
GPIO.setup(IN,GPIO.IN,pull_up_down = GPIO.PUD_UP)

i = 1
try:
    while True:
        if GPIO.input(IN)==GPIO.LOW:
            print("Pulsado !",i)
            GPIO.output(OUT,GPIO.HIGH)
        else:
            print("No pulsado !",i)
            GPIO.output(OUT,GPIO.LOW)
        time.sleep(0.5)
        i += 1
finally:
    GPIO.cleanup()