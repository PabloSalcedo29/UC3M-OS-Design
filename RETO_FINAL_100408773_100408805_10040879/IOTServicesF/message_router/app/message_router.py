import threading
import time, os, random, subprocess, json
import paho.mqtt.client as A
import requests
from flask import Flask, request
from flask_cors import CORS

index_room = 1
saved_rooms = {}


MQTT_SERVER = os.getenv("MQTT_SERVER_ADDRESS")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
DATA_INGESTION_API_URL = "http://" + os.getenv("DATA_INGESTION_API_HOST") + ":" + os.getenv("DATA_INGESTION_API_PORT")
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
TELEMETRY_TOPIC = "hotel/rooms/+/telemetry/"
TEMPERATURE_TOPIC = TELEMETRY_TOPIC + "temperature"
AIR_CONDITIONER_TOPIC = TELEMETRY_TOPIC + "air-conditioner"
PRESENCE_TOPIC = TELEMETRY_TOPIC + "presence"
IN_LIGHT_TOPIC = TELEMETRY_TOPIC + "in-light"
OUT_LIGHT_TOPIC = TELEMETRY_TOPIC + "out-light"
BLIND_TOPIC= TELEMETRY_TOPIC + "blind"
CONFIG_TOPIC = "hotel/rooms/+/config"
ALL_TOPICS = "hotel/rooms/+/telemetry/+"

app = Flask(__name__)


def on_connect(client, userdata, flags, rc):
    print("Connected on subscriber with code ", rc)
    client.subscribe(TEMPERATURE_TOPIC)
    print("Connected to ", TEMPERATURE_TOPIC)
    client.subscribe(AIR_CONDITIONER_TOPIC)
    print("Connected to ", AIR_CONDITIONER_TOPIC)
    client.subscribe(PRESENCE_TOPIC)
    print("Connected to ", PRESENCE_TOPIC)
    client.subscribe(IN_LIGHT_TOPIC)
    print("Connected to ", IN_LIGHT_TOPIC)
    client.subscribe(OUT_LIGHT_TOPIC)
    print("Connected to ", OUT_LIGHT_TOPIC)
    client.subscribe(BLIND_TOPIC)
    print("Connected to ", BLIND_TOPIC)
    client.subscribe(ALL_TOPICS)
    client.subscribe(CONFIG_TOPIC)
    print("Connected to all")
    print("Connected to ", CONFIG_TOPIC)


def on_message(client, userdate, msg):
    global index_room
    print("Mensaje recibido en ", msg.topic, " con mensaje " , msg.payload.decode())
    topic = msg.topic.split('/')
    if "config" in topic:
        room_name = "Room"+str(index_room)
        if (saved_rooms.get(msg.payload.decode()) == None):
            saved_rooms[msg.payload.decode()] = room_name
            print ("Digital with id ", msg.payload.decode(), "saved as", room_name)
            index_room = index_room + 1
            client.publish(msg.topic + "/room", payload=room_name, qos=0, retain=True)
            print("Publicado ", room_name, "en TOPIC", msg.topic)

    if "telemetry" in topic:
        room_name = topic[2]
        payload=json.loads(msg.payload)
        value=-1
        if topic[-1] == "temperature":
            value = payload["temperature"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": topic[-1], "value": value}
            )

        if topic[-1] == "air-conditioner":
            level = payload["air_conditioner"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "air-level", "value": level}
            )
            mode = payload["air_conditioner"]["active"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "air-mode", "value": mode}

            )
        if topic[-1] == "presence":
            value = payload["presence"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": topic[-1], "value": value}
            )
        if topic[-1] == "in-light":
            value = payload["in_light"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "in-light-level", "value": value}
            )
            mode = payload["in_light"]["active"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type":"in-light-mode", "value": mode}
            )
        if topic[-1] == "out-light":
            value = payload["out_light"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "out-light-level", "value": value}
            )
            mode = payload["out_light"]["active"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "out-light-mode", "value": mode}
            )
        if topic[-1] == "blind":
            value = payload["blind"]["value"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "blind-level", "value": value}
            )
            mode = payload["blind"]["active"]
            requests.post(
                DATA_INGESTION_API_URL+"/device_state",
                json = {"room": room_name, "type": "blind-mode", "value": mode}
            )


#{"air_conditioner": {"value":value}}
def send_command(params):
    type_dev = params["type"]
    value = params["value"]
    room = params["room"]
    topic = "hotel/rooms/"+room+"/command/air-conditioner"
    if type_dev == "air-conditioner-mode":
        client.publish(topic, payload = json.dumps({"air_conditioner": {"value":value}}), qos=0, retain=True)
        print("Command message sent through "+topic)
        return {"response":"Message successfully sent"},200
    else:
        return {"response":"Incorrect type param"}, 401

@app.route('/device_state', methods=['POST'])
def device_state():
    if request.method == 'POST':
        params = request.get_json()
        return send_command(params)
        

def mqtt_listener():
    client.loop_forever()


if __name__ == "__main__":
    client = A.Client()
    client.username_pw_set(username="dso_user", password="dso_password")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    t1 = threading.Thread(target=mqtt_listener)
    t1.setDaemon(True)
    t1.start()
    CORS(app)
    app.run(host=API_HOST, port=API_PORT, debug=True)


