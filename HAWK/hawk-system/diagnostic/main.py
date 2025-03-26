from flask import Flask, request
import requests
import logging
import time
import random

time.sleep(5)

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

GRIF_URL = "http://grif:8001/process"


@app.route("/confirm", methods=["POST"])
def diagnostic_event():
    data = request.json
    print(f"[Диагностика] Принял: {data["message"]}", flush=True)
    rand = bool(random.getrandbits(1))
    print("[Диагностика] Начал диагностику....", flush=True)
    
    message = "Diagnostic OK" if rand else "Diagnostic is not OK"
    if message == "Diagnostic OK":
        send_to_grif(message="Отключение питания Ветролова")

    return {"status": message}, 200

def send_to_grif(message):
    grif_data = requests.post(GRIF_URL, json={"source": "Диагностика", "message": message})
    print(f"[Диагностика] Отправлено в гриф {grif_data.json}", flush=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8006)