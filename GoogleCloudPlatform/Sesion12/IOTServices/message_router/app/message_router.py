import time, os, random, subprocess, json
import paho.mqtt.client as A
import requests

API_URL= "http://" + os.getenv("API_SERVER_ADDRESS") + ":" + os.getenv("API_SERVER_PORT")
room_name = 1
index_room = room_name
json_temperature = []
json_air = []
json_blind = []
current_temperature = "0"
current_air = "0"
current_blind = "0"
saved_rooms = {}

CONFIG_TOPIC = "hotel/room/+/config"

def on_connect1(client, userdata, flags, rc):
    print("Subscriber connected with code ", rc)
    client.subscribe("hotel/room/+/telemetry/+")
    print("Subscribed to TELEMETRY")
    client.subscribe(CONFIG_TOPIC)
    print("Subscribed to all")


def on_message1(client, userdate, msg):
    print("A")
    global current_temperature, current_air, current_blind, index_room, room_name
    print("Mensaje recibido en ", msg.topic, " con mensaje " , msg.payload.decode())
    topic = msg.topic.split('/')
    print(topic)
    if "config" in topic:
        print("B")
        if (saved_rooms.get(msg.payload.decode()) == None):
            room_name = "Room" + str(index_room)
            print ("Digital with id ", msg.payload.decode(), "saved as", room_name)
            index_room = index_room + 1
            client.publish(msg.topic + "/room", payload=room_name, qos=0, retain=True)

            print("Publicado ", room_name, "en TOPIC", msg.topic)

    if "telemetry" in topic:
        print("C")

        payload=json.loads(msg.payload)
        value=-1
        print(payload)
        for i in payload.values():
            value=i["value"]

        requests.post(
            API_URL + "/device_state",
            json={"room": topic[2], "type": topic[-1], "value": value}
        )

def openMqtt1(ip,usr,pwd):
    mqtt1 = A.Client()
    mqtt1.username_pw_set(username=usr,password=pwd)
    mqtt1.on_connect = on_connect1
    mqtt1.on_message = on_message1
    mqtt1.connect(ip,1883,60)
    return mqtt1



mqtt = openMqtt1("34.159.168.7", "dso_user", "dso_password")
mqtt.loop_forever()
