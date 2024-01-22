import os
import socket
import subprocess
import threading
import time, random
sensor = {}

HOST = os.getenv("VIRTUAL_ROOM_SERVER_ADDRESS")
PORT = int(os.getenv("VIRTUAL_ROOM_SERVER_PORT"))

def get_host_name():
    bashCommandName='echo $HOSTNAME'
    host = subprocess \
        .check_output(['bash', '-c', bashCommandName]) \
        .decode("utf-8")[0:-1]
    return host



def receive(conn, addr):
    with conn:
        print(f'Connected by {addr}. Waiting for messages')
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            else:
                print("Recibido", msg)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Escuchando en", get_host_name())
    s.bind((get_host_name(), PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=receive, args=(conn, addr)).start()
