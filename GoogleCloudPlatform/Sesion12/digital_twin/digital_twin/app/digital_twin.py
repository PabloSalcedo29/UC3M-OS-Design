import time, os, random, subprocess, json
import paho.mqtt.client as A

def get_host_name():
    bashCommandName='echo $HOSTNAME'
    host = subprocess.check_output(['bash', '-c', bashCommandName]).decode("utf-8")[0:-1]
    return host

ROOM_ID = get_host_name()
room_number = ""
sensors = {}

MQTT_SERVER = os.getenv("MQTT_SERVER_ADDRESS")
MQTT_PORT = int(os.getenv("MQTT_SERVER_PORT"))

CONFIG_TOPIC = "hotel/room/"+ROOM_ID+"/config"



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

def on_connect(client, userdata, flags, rc):
    print("Digital Twin connected with code ", rc)
    client.subscribe(CONFIG_TOPIC+"/room")
    print("Subscribed to", CONFIG_TOPIC+"/room")
    client.publish(CONFIG_TOPIC, payload=ROOM_ID, qos=0, retain=False)
    print("Enviado el id", ROOM_ID, "al topic", CONFIG_TOPIC)
    print(CONFIG_TOPIC)


def on_message(client, userdata, msg):
    global room_number
    room_number = msg.payload.decode()
    print("Room number received as:", room_number)


def on_publish(client, userdata, result):
    print("Data published")

client1 = A.Client()

def connect_mqtt1(client1):
    client1.username_pw_set(username="dso_user", password="dso_password")
    client1.on_connect = on_connect
    client1.on_message = on_message
    client1.on_publish = on_publish

    client1.connect("34.159.168.7", 1883, 60)
    return client1

client1.loop_start()
connect_mqtt1(client1)

while room_number ==  "":
    time.sleep(1)


"""
TELEMETRY_TOPIC = "hotel/room/" + room_number + "/telemetry"
TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air_conditioner"
BLIND_TOPIC = TELEMETRY_TOPIC + "/blind"
CONFIG_TOPIC1 = "hotel/room/"+room_number+"/config"
"""
index_room = 1
while True:
    room_name = "Room" + str(index_room)
    TELEMETRY_TOPIC = "hotel/room/" + room_name + "/telemetry"
    TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "/temperature"
    AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "/air_conditioner"
    BLIND_TOPIC = TELEMETRY_TOPIC + "/blind"
    CONFIG_TOPIC1 = "hotel/room/" + room_name + "/config"

    randomize_sensors()
    json_temperature = json.dumps({"temperature" : {"active": sensors["temperature"]["active"], "value": sensors["temperature"]["level"]}})
    json_air = json.dumps({"air_conditioner" : {"active": sensors["air_conditioner"]["active"], "value": sensors["air_conditioner"]["level"]}})
    json_blind = json.dumps({"blind" : {"active": sensors["blind"]["is_open"], "value": sensors["blind"]["level"]}})

    client1.publish(TEMPERATURE_TOPIC, payload=json_temperature, qos=0, retain=False)
    print("Published ", json_temperature, "in", TEMPERATURE_TOPIC)
    client1.publish(AIR_CONDITIONER_TOPIC, payload=json_air, qos=0, retain=False)
    print("Published", json_air, "in", AIR_CONDITIONER_TOPIC)
    client1.publish(BLIND_TOPIC, payload=json_blind, qos=0, retain=False)
    print("Published", json_blind, "in", BLIND_TOPIC)
    client1.publish(CONFIG_TOPIC1, payload=room_name, qos=0, retain=False)
    index_room = index_room +1

    time.sleep(2)


