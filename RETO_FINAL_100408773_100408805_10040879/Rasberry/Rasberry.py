import paho.mqtt.client as A
import Adafruit_DHT
import threading
import RPi.GPIO as GPIO
import time, json

# Datos para MQTT
MQTT_SERVER = "34.159.168.7"
MQTT_PORT = 1884
ROOM_ID = "Room1"
CONFIG_TOPIC = "hotel/rooms/"+ROOM_ID+"/config"
TELEMETRY_TOPIC = "hotel/rooms/"+ROOM_ID+"/telemetry"
COMMAND_TOPIC = "hotel/rooms/"+ROOM_ID+"/device_command"
TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
TEMPERATURE_TOPIC_COMMAND = COMMAND_TOPIC + "/temperature"
IN_LIGHT_TOPIC = TELEMETRY_TOPIC + "/in-light"
IN_LIGHT_TOPIC_COMMAND = COMMAND_TOPIC  + "/in-light"
OUT_LIGHT_TOPIC = TELEMETRY_TOPIC + "/out-light"
OUT_LIGHT_TOPIC_COMMAND = COMMAND_TOPIC + "/out-light"
BLIND_TOPIC = TELEMETRY_TOPIC + "/blind"
BLIND_TOPIC_COMMAND = COMMAND_TOPIC + "/blind"
AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air-conditioner"
AIR_CONDITIONER_TOPIC_COMMAND = COMMAND_TOPIC + "/air-conditioner"
PRESENCE_TOPIC = TELEMETRY_TOPIC + "/presence"
PRESENCE_TOPIC_COMMAND = COMMAND_TOPIC + "/presence"


GPIO.setmode(GPIO.BCM)
# Pins for Motor Driver Inputs
Motor1A = 23
Motor1B = 24
Motor1E = 25
# set red, green and blue pins
redPin = 16
greenPin = 22
bluePin = 27
# set button pin
BUTTON_GPIO = 26
# set Global variable
LEDColor = ""
# set Global variable
ButtonStatus = False
# set object from Lock
mutexLEDColor = threading.Semaphore(4)
client = A.Client()
# Initial the dht device, with data pin connected to:
DHT11 = 17
dhtDevice = Adafruit_DHT.DHT11
#luz interior y exterior
luzAzul = 12
luzAmarilla = 5
LUZ_EXTERIOR_ESTADO = False #apagada y encedida
LUZ_EXTERIOR_INTENSIDAD = 0
LUZ_INTERIOR_ESTADO  = False #apagada y encendida
LUZ_INTERIOR_INTENSIDAD  = 0
#persiana servo motor
servoMotor = 18

PERSIANA_ESTADO = "Open"
PERSIANA_VALOR = 0
GPIO.setmode(GPIO.BCM)
# GPIO Numbering
GPIO.setup(Motor1A, GPIO.OUT)
# All pins as Outputs
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(luzAzul, GPIO.OUT)
pwm_ledAzul = GPIO.PWM(luzAzul, 100)  # Dividimos en 100 partes por segundo
pwm_ledAzul.start(0)
GPIO.setup(luzAmarilla, GPIO.OUT)
pwm_ledAmarilla = GPIO.PWM(luzAmarilla, 100)
pwm_ledAmarilla.start(0)
pwmotor = GPIO.PWM(Motor1A, 100)
pwmotor.start(0)
contador = 0

humidity=0
AIRE_ESTADO = False
AIRE_INTENSIDAD = "off"
PRESENCE_STATE = 0

def nogira():
    global velocidad
    velocidad = "No gira"
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.LOW)

def gira10():
    global velocidad
    velocidad = "Gira 10%"
    GPIO.output(Motor1E, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    pwmotor.ChangeDutyCycle(10)


def gira60():
    global velocidad
    velocidad = "Gira 60%"
    GPIO.output(Motor1E, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    pwmotor.ChangeDutyCycle(60)


def gira80():
    global velocidad
    velocidad = "Gira 80%"
    GPIO.output(Motor1E, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    pwmotor.ChangeDutyCycle(80)
def white():
    global LEDColor, mutexLEDColor
    mutexLEDColor.acquire()
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)
    LEDColor = "white"
    time.sleep(1)
    mutexLEDColor.release()


def red():
    global LEDColor, mutexLEDColor
    mutexLEDColor.acquire()
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)
    LEDColor = "red"
    time.sleep(1)
    mutexLEDColor.release()


def blue():
    global LEDColor, mutexLEDColor
    mutexLEDColor.acquire()
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)
    LEDColor = "blue"
    time.sleep(1)
    mutexLEDColor.release()


def yellow():
    global LEDColor, mutexLEDColor
    mutexLEDColor.acquire()
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO. output(bluePin, GPIO.HIGH)
    LEDColor = "yellow"
    time.sleep(1)
    mutexLEDColor.release()


def green():
    global LEDColor, mutexLEDColor
    mutexLEDColor.acquire()
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)
    LEDColor = "green"
    time.sleep(1)
    mutexLEDColor.release()

def MotorDC(comando):
    global AIRE_INTENSIDAD, AIRE_ESTADO, mutexLEDColor
    while True:
        mutexLEDColor.acquire()
        if comando == "frio":
            gira80()
            blue()  # frio
            AIRE_ESTADO = True
            AIRE_INTENSIDAD = "frio"
        elif comando == "off":
            nogira()
            green()
            AIRE_ESTADO = False 
            AIRE_INTENSIDAD = "off"

        elif comando == "caliente":
            gira60()
            red()
            AIRE_ESTADO = True
            AIRE_INTENSIDAD = "caliente"
        else:
            nogira()
            turnOff()
        time.sleep(2.0)
        json_aire = json.dumps({"air_conditioner": {"active": AIRE_ESTADO, "value":  AIRE_INTENSIDAD}})
        client.publish(AIR_CONDITIONER_TOPIC, payload=json_aire, qos=0, retain=False)
        print("Published", AIRE_INTENSIDAD, "in", AIR_CONDITIONER_TOPIC)
        mutexLEDColor.release()

def turnOff():
    GPIO.output(redPin, GPIO.LOW)
    GPIO. output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)


def out_light(intensidad, orden):#intensidad va de 0 a 100 #azul
    #ordena va a ser si esta encendido o esta apagado
    global  LUZ_EXTERIOR_ESTADO, LUZ_EXTERIOR_INTENSIDAD, mutexLEDColor, pwn_ledAzul, luzAzul
    if orden == "encendido":
        pwm_ledAzul.ChangeDutyCycle(intensidad)  # va a ir de 0 a 100%
        LUZ_EXTERIOR_ESTADO = True  # apagada y encedida
        LUZ_EXTERIOR_INTENSIDAD = intensidad
        print("azul encendido")
    elif orden =="apagado":
        GPIO.output(luzAzul, GPIO.LOW)
        LUZ_EXTERIOR_ESTADO = False  # apagada y encedida
        LUZ_EXTERIOR_INTENSIDAD = 0
        print("azul apagada")
    json_luz_exterior = json.dumps({"out_light": {"active":  LUZ_EXTERIOR_ESTADO, "value": LUZ_EXTERIOR_INTENSIDAD}})
    client.publish(OUT_LIGHT_TOPIC, payload=json_luz_exterior, qos=0, retain=False)
    print("Published", LUZ_EXTERIOR_ESTADO, "in", OUT_LIGHT_TOPIC)



def in_light(intensidad, orden): #amarilla
    global LUZ_INTERIOR_ESTADO, LUZ_INTERIOR_INTENSIDAD, mutexLEDColor, pwn_ledAmarilla, luzAmarilla
    if orden == "encendido":
        pwm_ledAmarilla.ChangeDutyCycle(intensidad)  # va a ir de 0 a 100%
        LUZ_INTERIOR_ESTADO = True
        LUZ_INTERIOR_INTENSIDAD = intensidad
        print("amarilla encendido")
    elif orden == "apagado":
        GPIO.output(luzAmarilla, GPIO.LOW)
        LUZ_INTERIOR_ESTADO = False
        LUZ_INTERIOR_INTENSIDAD = 0
        print("amarilla apagada")
    json_luz_interior = json.dumps({"in_light": {"active": LUZ_INTERIOR_ESTADO, "value": LUZ_INTERIOR_INTENSIDAD}})
    client.publish(IN_LIGHT_TOPIC, payload=json_luz_interior, qos=0, retain=False)
    print("Published", LUZ_INTERIOR_ESTADO, "in", IN_LIGHT_TOPIC)


def activarServorMotor(posicion):#las posiciones las ponemos de 45 en 45 grados hasta 180 0-180 en intervalos de 45
    global PERSIANA_ESTADO,  PERSIANA_VALOR, mutexLEDColor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoMotor, GPIO.OUT)

    p = GPIO.PWM(servoMotor, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)

    if posicion == 0:
        p.ChangeDutyCycle(2.5)  # 0 ABIERTO
        PERSIANA_VALOR = 0
        PERSIANA_ESTADO = "Open"
    elif posicion == 45:
        p.ChangeDutyCycle(5)  # 45
        PERSIANA_VALOR = 45
        PERSIANA_ESTADO = "Open"
    elif posicion == 90:
        p.ChangeDutyCycle(7.5)  # 90
        PERSIANA_VALOR = 90
        PERSIANA_ESTADO = "Open"
    elif posicion == 135:
        p.ChangeDutyCycle(10)  # 135
        PERSIANA_VALOR = 135
        PERSIANA_ESTADO = "Open"
    elif posicion == 180:
        p.ChangeDutyCycle(12.5)  # 180 CERRADO
        PERSIANA_VALOR = 180
        PERSIANA_ESTADO = "Close"
    json_persiana = json.dumps({"blind":{"active": PERSIANA_ESTADO, "value":  PERSIANA_VALOR }})
    client.publish(BLIND_TOPIC, payload=json_persiana, qos=0, retain=False)
    print("Published", PERSIANA_ESTADO, "in", BLIND_TOPIC)


def auxiliar():
    global mutexLEDColor
    #recoger los mensajes y metrerlo en las funciones
    while True:
        mutexLEDColor.acquire()
        #recoja los mensajes y actualice las variables de entrada de las funciones
        out_light(20, "encendido")
        in_light(30,"encendido")
        activarServorMotor(90)
        MotorDC("caliente")
        time.sleep(2.0)
        mutexLEDColor.release()


def getReadDHTSensor():
    global mutexLEDColor, humidity
    while True:
        mutexLEDColor.acquire()
        humidity, temperature_c = Adafruit_DHT.read_retry(dhtDevice, DHT11)
        json_temperature = json.dumps({"temperature":{"active": True, "value": temperature_c}})
        #json_humidity = json.dumps({"humidity": int(humidity)})
        client.publish(TEMPERATURE_TOPIC, payload=json_temperature, qos=0, retain=False)
        print("Published", temperature_c, "in", TEMPERATURE_TOPIC)
        time.sleep(2.0)
        mutexLEDColor.release()


def setButtonPress():
    global ButtonStatus, contador, PRESENCE_STATE, mutexLEDColor, BUTTON_GPIO
    while True:
        mutexLEDColor.acquire()
        if GPIO.input(BUTTON_GPIO) == GPIO.LOW:
            contador = contador + 1
            time.sleep(0.2)
            if contador % 2 != 0:
                print("You are inside the room")
                ButtonStatus = True
                PRESENCE_STATE = 1
            else:
                print("You're leaving the room")
                ButtonStatus = False
                PRESENCE_STATE = 0
        json_presence = json.dumps({"presence": {"active": True, "value": PRESENCE_STATE}})
        client.publish(PRESENCE_TOPIC, payload=json_presence, qos=0, retain=False)
        print("Published", PRESENCE_STATE, "in", PRESENCE_TOPIC)
        time.sleep(2.0)
        mutexLEDColor.release()

def destroy():
    GPIO.cleanup()


def on_connect(client, userdata, flags, rc):
    print("Raspberry connected with code", rc)
    client.publish(CONFIG_TOPIC, payload=ROOM_ID, qos=0, retain=False)
    print("Enviado el id", ROOM_ID, "al topic", CONFIG_TOPIC)
    client.subscribe(OUT_LIGHT_TOPIC)
    print("Suscrito a  ", OUT_LIGHT_TOPIC)
    client.subscribe(IN_LIGHT_TOPIC)
    print("Suscrito a  ", IN_LIGHT_TOPIC)
    client.subscribe(BLIND_TOPIC)
    print("Suscrito a  ", BLIND_TOPIC)
    client.subscribe(AIR_CONDITIONER_TOPIC)
    print("Suscrito a  ", AIR_CONDITIONER_TOPIC)
    client.subscribe(PRESENCE_TOPIC)
    print("Suscrito a  ", PRESENCE_TOPIC)
    client.subscribe(AIR_CONDITIONER_TOPIC_COMMAND)
    client.subscribe(TEMPERATURE_TOPIC_COMMAND)
    client.subscribe(IN_LIGHT_TOPIC_COMMAND)
    client.subscribe(OUT_LIGHT_TOPIC_COMMAND)
    client.subscribe(BLIND_TOPIC_COMMAND)


def on_publish(client, userdata, result):
    print("Data published")

def suscribe():
    global client
    if client is not None:
        client.subscribe(OUT_LIGHT_TOPIC_COMMAND)
        print("Suscrito a  ", OUT_LIGHT_TOPIC_COMMAND)
        client.subscribe(IN_LIGHT_TOPIC_COMMAND)
        print("Suscrito a  ", IN_LIGHT_TOPIC_COMMAND)
        client.subscribe(BLIND_TOPIC_COMMAND)
        print("Suscrito a  ", BLIND_TOPIC_COMMAND)
        client.subscribe(AIR_CONDITIONER_TOPIC_COMMAND)
        print("Suscrito a  ", AIR_CONDITIONER_TOPIC_COMMAND)
        client.subscribe(PRESENCE_TOPIC_COMMAND)
        print("Suscrito a  ", PRESENCE_TOPIC_COMMAND)

def on_message(client, userdata, msg):
    topic = (msg.topic).split('/')
    print("MENSAJE RECIBIDOOOOOO FUNCION ONMESSAGEEEEEEEE")
    if "command" in topic:
        payload = json.loads(msg.payload)
        if topic[-1] == "air_conditioner":
            MotorDC(payload["value"]) #cold #hot #off
        if topic[-1] == "out_light":
            out_light(payload["value"], payload["active"])
        if topic[-1] == "in_light":
            in_light(payload["value"], payload["active"])
        if topic[-1] == "blind":
            activarServorMotor(payload["value"])

def connect_mqtt():
    global client, MQTT_PORT, MQTT_SERVER
    client.username_pw_set(username="dso_user", password="dso_password")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    #aqui falta el on message
    client.connect("34.159.168.7", 1884, 60)
    #conect channels no se que es
    print("MQTT conected")






def main():
    connect_mqtt()
    try:
        #t1 = threading.Thread(target=MotorDC)
        #t2 = threading.Thread(target=LED_RGB)
        #t3 = threading.Thread(target=getLEDValue)
        t4 = threading.Thread(target=getReadDHTSensor)
        t5 = threading.Thread(target=setButtonPress)
        #hacer funcion  que llame a la persiana y a la luces interiores y exterior
        #luz interior
        #luz exterior
        #persiana
        t6 = threading.Thread(target=auxiliar)

        #t1.setDaemon(True)
        #t2.setDaemon(True)
        #t3.setDaemon(True)
        t4.setDaemon(True)
        t5.setDaemon(True)
        t6.setDaemon(True)

        #t1.start()
        #t2.start()
        #t3.start()
        t4.start()
        t5.start()
        t6.start()

        #t1.join()
        #t2.join()
        #t3.join()
        t4.join()
        t5.join()
        t6.join()

    except Exception as e:
        print(e)
    finally:
        destroy()


if __name__ == '__main__':
    main()
