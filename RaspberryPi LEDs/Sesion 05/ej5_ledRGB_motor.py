import threading
import random
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



redPin = 17
greenPin = 27
bluePin = 22
Motor1A = 23
Motor1B = 24
Motor1E = 25

luz = ""
velocidad = ""
sem = threading.Semaphore()
numeroAleatorio = random.randint(0, 2)


GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)



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
    luz = "Azul"
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)


# Activamos azul
def azul():
    global luz
    luz = "Verde"
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)


# Activamos gira a un lado
def giraLado1():
    global velocidad
    velocidad = "Gira lado 1"
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)


# Activamos gira al otro lado
def giraLado2():
    global velocidad
    velocidad = "Gira lado 2"
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)


# Funcion que enciende las luces-- hiloLed
def encenderLuz():
    global numeroAleatorio
    if numeroAleatorio == 0:
        rojo()
    elif numeroAleatorio == 1:
        verde()
    elif numeroAleatorio == 2:
        azul()


def apagar():
    global velocidad
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.LOW)


# Funcion que activa el motor -- hiloMotor
def funcionamientoMotor():
    global numeroAleatorio
    while True:
        if numeroAleatorio == 0:
            apagar()
        elif numeroAleatorio == 1:
            sem.acquire()
            giraLado1()
            sem.release()
            time.sleep(1)
        elif numeroAleatorio == 2:
            sem.acquire()
            giraLado2()
            sem.release()
            time.sleep(1)


def imprimos():
    while True:
        print("Led " + luz + " a velocidad " + velocidad)


def ejecutar():
    try:
        while True:
            hiloLed = threading.Thread(target=encenderLuz)
            hiloMotor = threading.Thread(target=funcionamientoMotor)
            hiloImprimir = threading.Thread(target=imprimos, daemon=True)

            hiloLed.start()
            hiloMotor.start()
            hiloImprimir.start()
            hiloLed.join()
            hiloMotor.join()
    finally:
        GPIO.cleanup()

ejecutar()