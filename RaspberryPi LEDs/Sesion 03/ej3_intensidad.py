import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
pwm= GPIO.PWM(18,100)
pwm.start(0)

for i in range(10):
    for intensidad in range(0,101,20):
        print(intensidad)
        pwm.ChangeDutyCycle(intensidad)
        time.sleep(0.5)

GPIO.cleanup()
