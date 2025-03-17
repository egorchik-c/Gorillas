from flask import Flask, request
import requests
import logging

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

GRIF_URL = "http://grif:8001/process"



@app.route("/motion", methods=["POST"])

def receive_motion():
    data = request.json
    print(f"[Волан] Принято от ромашки: {data}")

    volan_log = {"source": "Волан", "message": data}
    grif_data = requests.post(GRIF_URL, json=volan_log)
    print(f"[Волан]Отправлено в Гриф: {volan_log}", flush=True)
    
    return {"status": "SEND_TO_GRIF"}, grif_data.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)