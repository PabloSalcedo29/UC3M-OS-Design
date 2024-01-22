import os
import socket
import time, random
sensors = {}

HOST = os.getenv("VIRTUAL_ROOM_SERVER_ADDRESS")
PORT = int(os.getenv("VIRTUAL_ROOM_SERVER_PORT"))
def randomize_sensors():
    global sensors
    sensors = {
        "luz_interior":{
            "active":True if random.randint(0,1) == 1 else False,
            "level":random.randint(0,100)
        },
        "luz_exterior": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 100)
        },
        "blind": {
            "is_open": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 100)
        },
        "aire_acondicionado": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(10, 30)
        },
        "presencia": {
            "active": True if random.randint(0, 1) == 1 else False,
            "detected": random.randint(0, 1)
        },
        "temperatura": {
            "active": True if random.randint(0, 1) == 1 else False,
            "level": random.randint(0, 40)
        }
    }
def get_sensors_state():
    my_bytes = bytearray()
    my_bytes.append(sensors["luz_interior"]["active"])
    my_bytes.append(sensors["luz_interior"]["level"])
    my_bytes.append(sensors["luz_exterior"]["active"])
    my_bytes.append(sensors["luz_exterior"]["level"])
    my_bytes.append(sensors["blind"]["is_open"])
    my_bytes.append(sensors["blind"]["level"])
    my_bytes.append(sensors["aire_acondicionado"]["active"])
    my_bytes.append(sensors["aire_acondicionado"]["level"])
    my_bytes.append(sensors["presencia"]["active"])
    my_bytes.append(sensors["presencia"]["detected"])
    my_bytes.append(sensors["temperatura"]["active"])
    my_bytes.append(sensors["temperatura"]["level"])
    return my_bytes


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Conectando con HOST", HOST, "en el puerto", PORT)
    s.connect((HOST,PORT))
    while True:
        randomize_sensors()
        msg=get_sensors_state()
        print("Enviando", msg)
        s.sendall(msg)
        time.sleep(3)
