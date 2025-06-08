# health_server.py
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/health")
def health():
    return "OK", 200

def run_server():
    app.run(host="0.0.0.0", port=8080)

def start_health_server():
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
