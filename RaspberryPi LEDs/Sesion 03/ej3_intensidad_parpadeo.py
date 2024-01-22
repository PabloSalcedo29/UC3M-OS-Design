import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
pwm= GPIO.PWM(18,100)
pwm.start(0)
potencia = 0

try:
    while True:
        for potencia in range(0,101,20):
            pwm.ChangeDutyCycle(potencia)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.5)
            print(potencia)

        for potencia in range(95,0,-20):
            pwm.ChangeDutyCycle(potencia)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.5)
            print(potencia)
except KeyboardInterrupt:
    print("Programa parado")

pwm.stop()