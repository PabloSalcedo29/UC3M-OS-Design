import RPi.GPIO as GPIO
import sys
import signal

def theend(sig, frame):
    print("limpiando todo para salir...")
    GPIO.cleanup()
    sys.exit()

def click(channel):
    if GPIO.input(IN) == GPIO.LOW:
        print("ON")
        GPIO.output(OUT,GPIO.HIGH)
    else:
        print("OFF")
        GPIO.output(OUT,GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN = 16
OUT = 20
GPIO.setup(IN,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(OUT,GPIO.OUT)
GPIO.add_event_detect(IN, GPIO.BOTH, callback = click, bouncetime = 100)
signal.signal(signal.SIGINT,theend)
signal.pause()