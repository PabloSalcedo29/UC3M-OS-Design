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
        GPIO.wait_for_edge(IN,GPIO.BOTH) #puedes poner falling
        if GPIO.input(IN)==GPIO.LOW:
            for i in range(10):
                print("ON: ", i + 1)
                GPIO.output(OUT, GPIO.HIGH)
                time.sleep(1)
                print("OFF: ", i + 1)
                GPIO.output(OUT, GPIO.LOW)
                time.sleep(1)
        else:
            print("OFF")
            GPIO.output(OUT,GPIO.LOW)

finally:
    GPIO.cleanup()