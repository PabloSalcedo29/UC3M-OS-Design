import time, os, random, subprocess, json
import paho.mqtt.client as A
index_room = 1
json_temperature = []
json_air = []
json_blind = []
current_temperature = "0"
current_air = "0"
current_blind = "0"
saved_rooms = {}


def on_connect(client, userdata, flags, rc):
    print("Subscriber connected with code ", rc)
    client.subscribe("hotel/rooms/+/telemetry/+")
    print("Subscribed to TELEMETRY")
    client.subscribe("hotel/rooms/+/config")
    print("Subscribed to all")

def on_message(client, userdate, msg):
    global current_temperature, current_air, current_blind, index_room
    print("Mensaje recibido en ", msg.topic, " con mensaje ", msg.payload.decode())
    topic = (msg.topic).split('/')
    if topic[-1] == "config":
        if (saved_rooms.get(msg.payload.decode()) == None):
            room_name = "Room"+str(index_room)
            saved_rooms[msg.payload.decode()] = room_name
            print("Digital with id", msg.payload.decode(), "saved as", room_name)
            index_room+=1
            client.publish(msg.topic+"/room", payload=room_name, qos=0, retain=True)
            print("Publicado", room_name, "en TOPIC", msg.topic)

        if topic[-1] == "temperature":
            current_temperature = msg.payload.decode()
            json_temperature.append(current_temperature)
            with open('temperature.json', 'w') as json_file:
                json.dump(json_temperature, json_file)

        if topic[-1] == "air_conditioner":
            current_air = msg.payload.decode()
            json_air.append(current_air)
            with open('air-conditioner.json', 'w') as json_file:
                json.dump(json_air, json_file)

        if topic[-1] == "blind":
            current_blind = msg.payload.decode()
            json_air.append(current_blind)
            with open('blind.json', 'w') as json_file:
                json.dump(json_blind, json_file)


def openMqtt(ip,usr,pwd):
    mqtt = A.Client()
    mqtt.username_pw_set(username=usr,password=pwd)
    mqtt.on_connect = on_connect
    mqtt.on_message = on_message
    mqtt.connect(ip,1883,60)
    return mqtt

mqtt= openMqtt("34.159.168.7", "dso_user", "dso_password")
mqtt.loop_forever()