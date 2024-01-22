import Adafruit_DHT
import threading
import random
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensor = Adafruit_DHT.DHT11
redPin = 17
greenPin = 22
bluePin = 27
Motor1A = 23
Motor1B = 24
Motor1E = 25
sensor_gpio = 4
boton_gpio = 21

luz = ""
velocidad = ""

GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(boton_gpio,GPIO.IN,pull_up_down = GPIO.PUD_UP)

humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)

def humedad_led():
    i=2
    while True:
        if GPIO.input(boton_gpio) == GPIO.LOW and i%2==0: #para que funcione hay que mantener presionado el boton
            humidity, temperature= Adafruit_DHT.read(sensor,sensor_gpio)
            if humidity is not None and temperature is not None:
                if humidity <= 45:
                    verde()
                elif 45 < humidity <= 55:
                    azul()
                elif humidity > 55:
                    rojo()
            else:
                print("Error de medicion")
        else:
            apagar()


def humedad_motor():
    i = 2
    while True:
        if GPIO.input(boton_gpio) == GPIO.LOW and i%2==0: #para que funcione hay que mantener presionado el boton
            humidity, temperature= Adafruit_DHT.read(sensor,sensor_gpio)
            if humidity is not None and temperature is not None:
                if humidity <= 45:
                    giraLento()
                elif 45 < humidity <= 55:
                    giraMedio()
                elif humidity > 55:
                    giraRapido()

            else:
                print("Error de medicion")
        else:
            apagar()


# Activamos rojo
def rojo():
    global luz
    luz = "Rojo"
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)


# Activamos verde
def verde():
    global luz
    luz = "Verde"
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)


# Activamos azul
def azul():
    global luz
    luz = "Azul"
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)

lado1=GPIO.PWM(Motor1A,100)
lado2=GPIO.PWM(Motor1B,100)

# Activamos gira velocidad lenta
def giraLento():
    global velocidad
    velocidad = "Gira a velocidad lenta"
    lado1.start(0)
    lado2.start(0)
    lado1.ChangeDutyCycle(20)
    lado2.ChangeDutyCycle(0)
    GPIO.output(Motor1E, GPIO.HIGH)

# Activamos gira velocidad media
def giraMedio():
    global velocidad
    velocidad = "Gira a velocidad media"
    lado1.start(0)
    lado2.start(0)
    lado1.ChangeDutyCycle(50)
    lado2.ChangeDutyCycle(0)
    GPIO.output(Motor1E, GPIO.HIGH)


# Activamos gira velocidad rapida
def giraRapido():
    global velocidad
    velocidad = "Gira a velocidad rapida"
    lado1.start(0)
    lado2.start(0)
    lado1.ChangeDutyCycle(95)
    lado2.ChangeDutyCycle(0)
    GPIO.output(Motor1E, GPIO.HIGH)


def apagar():
    global velocidad
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)


def imprimos():
    while True:
        print("Led " + luz + " a velocidad " + velocidad)
        print('Temperatura = {0:0.1f}*C  Humedad = {1:0.1f}%'.format(temperature, humidity))



def ejecutar():
    try:
        hilohumedad_led = threading.Thread(target=humedad_led)
        hilohumedad_motor = threading.Thread(target=humedad_motor)
        hiloImprimir = threading.Thread(target=imprimos, daemon=True)
        hilohumedad_led.start()
        hilohumedad_motor.start()
        hiloImprimir.start()
        hilohumedad_led.join()
        hilohumedad_motor.join()
    finally:
        GPIO.cleanup()

ejecutar()