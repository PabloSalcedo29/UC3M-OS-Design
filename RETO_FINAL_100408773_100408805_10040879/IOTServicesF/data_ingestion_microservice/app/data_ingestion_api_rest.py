from flask import Flask, request
from flask_cors import CORS
from data_ingestion import insert_device_state, get_device_state
import os

app = Flask(__name__)
CORS(app)

@app.route('/device_state', methods=['GET','POST'])
def device_state():
    if request.method == 'POST':
        params = request.get_json()
        if len(params) != 3:
            return {"response":"Incorrect parameters"}, 401
        mycursor = insert_device_state(params)
        return {"response":"records inserted."}, 200
    elif request.method == 'GET':
        return get_device_state(), 200

HOST = os.getenv('HOST')
PORT = os.getenv('POST')
app.run(host=HOST, port=PORT, debug=True)
