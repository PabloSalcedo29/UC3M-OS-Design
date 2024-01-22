import time, os, random, subprocess, json
import threading
import paho.mqtt.client as mqtt


def get_host_name():
    bashCommandName='echo $HOSTNAME'
    host = subprocess.check_output(['bash', '-c', bashCommandName]).decode("utf-8")[0:-1]
    return host

#VARIABLES 
RANDOMIZE_SENSORS_INTERVAL = 60
MQTT_SERVER = os.getenv("MQTT_SERVER_ADDRESS")
MQTT_PORT_1 = int(os.getenv("MQTT_SERVER_PORT_1"))
MQTT_PORT_2 = int(os.getenv("MQTT_SERVER_PORT_2"))
ROOM_ID = get_host_name()
CONFIG_TOPIC = "hotel/rooms/"+ROOM_ID+"/config"
AIR_CONDITIONER_COMMAND_TOPIC = "hotel/rooms/" + ROOM_ID + "/config"

room_number = ""
flag = 0

sensors = {}

temperature = 0
current_temperature = 0
air_conditioner_level = 0
current_air_conditioner_level = 0
air_conditioner_mode = 0
current_air_conditioner_mode = 0 
presence = 0
current_presence = 0
in_light_level = 0
in_light_mode = 0
current_in_light_level = 0
current_in_light_mode= 0
out_light_level = 0
out_light_mode = 0
current_out_light_level = 0
current_out_light_mode = 0
blind_level= 0
blind_mode = 0
current_blind_level= 0
current_blind_mode =0


def on_connect_1883(client, userdata, flags, rc):
    print("MQTT 1883 connected wuth code", rc, "THREAD", threading.current_thread().ident)
    client.publish(CONFIG_TOPIC, payload=ROOM_ID, qos=0, retain=False)
    print("Enviado MQTT 1883 el id", ROOM_ID, "al topic", CONFIG_TOPIC)
    client.subscribe(CONFIG_TOPIC + "/room")

    TELEMETRY_TOPIC = "hotel/rooms/" + room_number + "/telemetry"
    TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
    AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air-conditioner"
    PRESENCE_TOPIC = TELEMETRY_TOPIC + "/presence"
    IN_LIGHT = TELEMETRY_TOPIC + "/in-light"
    OUT_LIGHT = TELEMETRY_TOPIC + "/out-light"
    BLIND = TELEMETRY_TOPIC + "/blind"
    AIR_CONDITIONER_COMMAND_TOPIC = "hotel/rooms/" + room_number + "/command/air-conditioner"
    client.subscribe(AIR_CONDITIONER_COMMAND_TOPIC)
    print("Suscrito a MQTT 1883 to", AIR_CONDITIONER_COMMAND_TOPIC)
    print("Topic is", TELEMETRY_TOPIC, "in thread", threading.current_thread().ident)

def on_message_1883(client, userdata, msg):
    print("Mensaje recibido en MQTT 1883", msg.topic, "con  mensajes ", msg.payload.decode())
    topic = (msg.topic).split('/')
    if "config" in topic:
        global room_number
        room_number = msg.payload.decode()
        print("Room number received as: ", room_number, "in thread", threading.current_thread().ident)

    elif "command" in topic:
        if topic[-1] == "air-conditioner":
            global air_conditioner_mode
            print("RECIBIDA COMANDO DE AIRE ACONDICIONADO")
            payload = json.loads(msg.payload)
            air_conditioner_mode = payload["mode"]

def on_connect_1884(client, userdata, flags, rc):
    print("Connected to MQTT 1884 with code", rc, "THREAD", threading.current_thread().ident)
    CONFIG_TOPIC_1884 = "hotel/rooms/" + room_number + "/config"
    client.subscribe(CONFIG_TOPIC_1884)
    TELEMETRY_TOPIC = "hotel/rooms/" + room_number + "/telemetry"
    TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
    AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air-conditioner"
    PRESENCE_TOPIC = TELEMETRY_TOPIC + "/presence"
    IN_LIGHT_TOPIC = TELEMETRY_TOPIC + "/in-light"
    OUT_LIGHT_TOPIC = TELEMETRY_TOPIC + "/out-light"
    BLIND_TOPIC= TELEMETRY_TOPIC + "/blind"
    AIR_CONDITIONER_COMMAND_TOPIC = "hotel/rooms/" + room_number + "/command/air-conditioner"
    client.subscribe(TEMPERATURE_TOPIC)
    client.subscribe(AIR_CONDITIONER_TOPIC)
    client.subscribe(PRESENCE_TOPIC)
    client.subscribe(IN_LIGHT_TOPIC)
    client.subscribe(OUT_LIGHT_TOPIC)
    client.subscribe(BLIND_TOPIC)
    print("Suscrito a ", TEMPERATURE_TOPIC)
    print("Suscrito a ", AIR_CONDITIONER_TOPIC)
    print("Suscrito a ", PRESENCE_TOPIC)
    print("Suscrito a ", IN_LIGHT_TOPIC)
    print("Suscrito a ", OUT_LIGHT_TOPIC)
    print("Suscrito a ", BLIND_TOPIC)

def on_message_1884(client, userdata, msg):
    global temperature, air_conditioner_level, air_conditioner_mode, presence, room_number, in_light_level, in_light_mode, out_light_level, out_light_mode, blind_level, blind_mode
    print("Mensaje recibido en MQTT 1884", msg.topic, "con mensaje", msg.payload.decode())
    topic = (msg.topic).split('/')
    if "temperature" in topic:
        print("Recibida temperatura")
        payload = json.loads(msg.payload)
        temperature=payload["temperature"]["value"]
    if topic[-1] == "air-conditioner": 
        print("Recibida aire condicionado")
        payload = json.loads(msg.payload)
        air_conditioner_mode=payload["air_conditioner"]["active"]
        air_conditioner_level=payload["air_conditioner"]["value"]
    if topic[-1] == "presence": 
        print("Recibida presencia")
        payload = json.loads(msg.payload)
        presence=payload["presence"]["value"]
    if topic[-1] == "in_light": 
        print("Recibida luz interior")
        payload = json.loads(msg.payload)
        in_light_mode = payload["in_light"]["active"]
        in_light_level=payload["in_light"]["value"]
    if topic[-1] == "out_light": 
        print("Recibida luz exterior")
        payload = json.loads(msg.payload)
        out_light_mode = payload["out_light"]["active"]
        out_light_level=payload["out_light"]["value"]
    if topic[-1] == "blind": 
        print("Recibida persiana")
        payload = json.loads(msg.payload)
        blind_mode = payload["blind"]["active"]
        blind_level=payload["blind"]["value"]
    if topic[-1] == "config":
        new_topic = "hotel/rooms/" + room_number + "/config/room"
        client.publish(new_topic, payload= room_number, qos=0, retain=False)
        print("Enviado id por ", new_topic)

def randomize_sensors():
    global sensors
    sensors = {
        "in_light": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 100)
        },
        "out_light": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 100)
        },
        "blind": {
            "is_open": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 100)
        },
        "air_conditioner": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(10, 30)
        },
        "presence": {
            "active": True if random.randint(0, 1) == 1 else False,
            "detected": random.randint(0, 1)
        },
        "temperature": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 40)
        }
    }

def execute_thread_2():
    global air_conditioner_mode, current_air_conditioner_mode,room_number
    while room_number == "": 
        print("Esperando room number en hilo ", threading.current_thread().ident)
        time.sleep(1)
    CONFIG_TOPIC = "hotel/rooms/" + room_number + "/config"
    client=mqtt.Client()
    client.username_pw_set(username="dso_user", password="dso_password")
    client.on_connect=on_connect_1884
    client.on_message=on_message_1884
    client.connect(MQTT_SERVER, MQTT_PORT_2, 60)
    client.loop_start()
    while True:
        if current_air_conditioner_mode != air_conditioner_mode:
            client.publish(
                AIR_CONDITIONER_COMMAND_TOPIC,
                payload = json.dumps({"mode":air_conditioner_mode}),
                qos=0,
                retain=False)
            print("Publicado", air_conditioner_mode, "in", AIR_CONDITIONER_COMMAND_TOPIC)
            time.sleep(1)
    client.loop_stop()

def execute_thread_1():
    global temperature, current_temperature
    global air_conditioner_level, current_air_conditioner_level
    global air_conditioner_mode, current_air_conditioner_mode
    global presence, current_presence
    global current_in_light_level, current_in_light_mode, current_out_light_level, current_out_light_mode, current_blind_level, current_blind_mode
    global in_light_mode, in_light_level, out_light_mode, out_light_level, blind_mode, blind_level
    client=mqtt.Client()
    client.username_pw_set(username="dso_user", password="dso_password")
    client.on_connect=on_connect_1883
    client.on_message=on_message_1883
    client.on_disconnect = on_disconnect
    client.connect(MQTT_SERVER, MQTT_PORT_1, 60)
    client.loop_start()
    while room_number == "": 
        print("Esperando room number en hilo ", threading.current_thread().ident)
        time.sleep(1)
    CONFIG_TOPIC = "hotel/rooms/" + room_number + "/config"
    TELEMETRY_TOPIC = "hotel/rooms/" + room_number + "/telemetry"
    TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
    AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air-conditioner"
    PRESENCE_TOPIC = TELEMETRY_TOPIC + "/presence"
    IN_LIGHT_TOPIC = TELEMETRY_TOPIC + "/in-light"
    OUT_LIGHT_TOPIC = TELEMETRY_TOPIC + "/out-light"
    BLIND_TOPIC = TELEMETRY_TOPIC + "/blind"
    AIR_CONDITIONER_COMMAND_TOPIC =  "hotel/rooms/" + room_number + "/command/air-conditioner"

    while True:
        print("generar aleatorios")
        randomize_sensors()
        temperature = sensors["temperature"]["level"]
        air_conditioner_level = sensors["air_conditioner"]["level"]
        air_conditioner_mode = sensors["air_conditioner"]["active"]
        presence = sensors["presence"]["detected"]
        in_light_level = sensors["in_light"]["level"]
        in_light_mode = sensors["in_light"]["active"]
        out_light_level = sensors["out_light"]["level"]
        out_light_mode = sensors["out_light"]["active"]
        blind_level= sensors["blind"]["level"]
        blind_mode= sensors["blind"]["is_open"]

        json_temperature = json.dumps({"temperature" : {"active": sensors["temperature"]["active"], "value": sensors["temperature"]["level"]}})
        json_air = json.dumps({"air_conditioner" : {"active": sensors["air_conditioner"]["active"], "value": sensors["air_conditioner"]["level"]}})
        json_blind = json.dumps({"blind" : {"active": sensors["blind"]["is_open"], "value": sensors["blind"]["level"]}})
        json_presence = json.dumps({"presence" : {"active": sensors["presence"]["active"], "value": sensors["presence"]["detected"]}})
        json_out_light = json.dumps({"out_light" : {"active": sensors["out_light"]["active"], "value": sensors["out_light"]["level"]}})
        json_in_light = json.dumps({"in_light" : {"active": sensors["in_light"]["active"], "value": sensors["in_light"]["level"]}})
        if temperature != current_temperature:
            client.publish(TEMPERATURE_TOPIC, payload=json_temperature, qos=0, retain=False)
            print("PUBLISHED", temperature,"IN", TEMPERATURE_TOPIC)
            current_temperature = temperature
        if air_conditioner_level != current_air_conditioner_level or air_conditioner_mode != current_air_conditioner_mode:
            client.publish(
                AIR_CONDITIONER_TOPIC,
                payload= json_air,
                qos=0, retain=False
            )
            print("PUBLISHED", str(air_conditioner_level)+ "," + str(air_conditioner_mode), "IN", AIR_CONDITIONER_TOPIC)
            current_air_conditioner_level = air_conditioner_level
            current_air_conditioner_mode = air_conditioner_mode
        if presence != current_presence:
            client.publish(PRESENCE_TOPIC,payload= json_presence,qos=0,retain=False)
            print("PUBLISHED",presence,"IN", PRESENCE_TOPIC)
            current_presence = presence
        if in_light_level != current_in_light_level or in_light_mode != current_in_light_mode: 
            client.publish(IN_LIGHT_TOPIC,payload= json_in_light,qos=0,retain=False)
            print("PUBLISHED",str(in_light_level)+ "," + str(in_light_mode),"IN", IN_LIGHT_TOPIC)
            current_in_light_level = in_light_level
            current_in_light_mode = in_light_mode
        if out_light_level != current_out_light_level or out_light_mode != current_out_light_mode:
            client.publish(OUT_LIGHT_TOPIC, payload=json_out_light, qos=0, retain=False)
            print("PUBLISHED", str(out_light_level)+ "," + str(out_light_mode),"IN", OUT_LIGHT_TOPIC)
            current_out_light_level = out_light_level
            current_out_light_mode = out_light_mode
        if blind_level!= current_blind_level or blind_mode != current_blind_mode:
            client.publish(BLIND_TOPIC, payload=json_blind, qos=0, retain=False)
            print("PUBLISHED",str(blind_level)+ "," + str(blind_mode),"IN", BLIND_TOPIC)
            current_blind_level = blind_level
            current_blind_mode = blind_mode
        time.sleep(20)
    client.loop_stop()


def on_disconnect(client,userdata,rc):
    global flag
    flag = -1

if __name__=="__main__":
    t1 = threading.Thread(target=execute_thread_1)
    t2 = threading.Thread(target=execute_thread_2)

    t1.setDaemon(True)
    t2.setDaemon(True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

"""while True:
    room_name = room_number
    TELEMETRY_TOPIC = "hotel/rooms/" + room_name + "/telemetry"
    TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
    AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air_conditioner"
    BLIND_TOPIC = TELEMETRY_TOPIC + "/blind"
    PRESENCE_TOPIC = TELEMETRY_TOPIC + "/presence"
    OUT_LIGHT_TOPIC = TELEMETRY_TOPIC + "/out_light"
    IN_LIGHT_TOPIC = TELEMETRY_TOPIC + "/in_light"

    randomize_sensors()
    json_temperature = json.dumps({"temperature" : {"active": sensors["temperature"]["active"], "value": sensors["temperature"]["level"]}})
    json_air = json.dumps({"air_conditioner" : {"active": sensors["air_conditioner"]["active"], "value": sensors["air_conditioner"]["level"]}})
    json_blind = json.dumps({"blind" : {"active": sensors["blind"]["is_open"], "value": sensors["blind"]["level"]}})
    json_presence = json.dumps({"presence" : {"active": sensors["presence"]["active"], "value": sensors["presence"]["detected"]}})
    json_out_light = json.dumps({"out_light" : {"active": sensors["out_light"]["active"], "value": sensors["out_light"]["level"]}})
    json_in_light = json.dumps({"in_light" : {"active": sensors["in_light"]["active"], "value": sensors["in_light"]["level"]}})

    client1.publish(TEMPERATURE_TOPIC, payload=json_temperature, qos=0, retain=False)
    print("Published ", json_temperature, "in", TEMPERATURE_TOPIC)
    client1.publish(AIR_CONDITIONER_TOPIC, payload=json_air, qos=0, retain=False)
    print("Published", json_air, "in", AIR_CONDITIONER_TOPIC)
    client1.publish(BLIND_TOPIC, payload=json_blind, qos=0, retain=False)
    print("Published", json_blind, "in", BLIND_TOPIC)
    client1.publish(PRESENCE_TOPIC, payload=json_presence, qos=0, retain=False)
    print("Published ", json_presence, "in",PRESENCE_TOPIC)
    client1.publish(OUT_LIGHT_TOPIC, payload=json_out_light, qos=0, retain=False)
    print("Published ", json_out_light, "in", OUT_LIGHT_TOPIC)
    client1.publish(IN_LIGHT_TOPIC, payload=json_in_light, qos=0, retain=False)
    print("Published ", json_in_light, "in", IN_LIGHT_TOPIC)
    time.sleep(5)"""


