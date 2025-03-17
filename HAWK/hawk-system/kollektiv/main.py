from flask import Flask, request
import requests
import logging

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

@app.route("/log", methods=["POST"])

def receive_logs():
    data = request.json
    print(f"[Коллектив] Принял отчет: {data["message"]}", flush=True)

    return {"status": "LOG_SAVED"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)