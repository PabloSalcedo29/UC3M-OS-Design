import mysql.connector, json, os, sys
from datetime import datetime, date
from flask import Flask, request
from flask_cors import CORS

def connect_database():
    print("Datos de conexion: ", os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
    mydb=mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return mydb

def insert_device_state(params):
    mydb=connect_database()
    with mydb.cursor() as mycursor:
        sql="INSERT INTO device_state (room, type, value, date) VALUES (%s,%s,%s,%s)"

        values=(
            params["room"],
            params["type"],
            params["value"],
            datetime.now()
        )
        print(sql, values)
        mycursor.execute(sql, values)
        mydb.commit()
        return mycursor

app=Flask(__name__)
CORS(app)

@app.route('/device_state', methods=['GET', 'POST'])
def device_state():
    if request.method=='POST':
        params=request.get_json()
        if len(params)!=3:
            return {"response":"Incorrect parameters"}, 401
        mycursor=insert_device_state(params)
        return {"response":f"{mycursor.rowcount} records inserted"}, 200



HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
app.run(host=HOST, port=PORT, debug=True)