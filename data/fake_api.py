from flask import Flask, jsonify
import random
import datetime
import requests

def fetch_data():
    url = "http://localhost:5000/data"
    r = requests.get(url,timeout=2)
    return r.json()

app = Flask(__name__)

#inizio simulazione turbina industriale
def generate_sensor_data():
    return {
        "time": datetime.datetime.now().isoformat(),
        "temperature": round(random.uniform(60,95), 2), #check temperatura
        "pressure": round(random.uniform(100, 1000), 2),#check pressione
        "fault": 1 if random.random()> 0.95 else 0, #check guasto   
        "rul": round(random.uniform(0, 100), 2) #check rul simulato
    }
    
 #endpoint API per dati simulati
@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(generate_sensor_data())

#avvio del server di flask
if __name__ == "__main__":
    app.run(debug=True, port=5000) 