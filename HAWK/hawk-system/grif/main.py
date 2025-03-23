from flask import Flask, request
import requests
import logging
import time

time.sleep(3)

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

KOLLEKTIV_URL = "http://kollektiv:8002/log"

@app.route("/process", methods=["POST"])
def process_event():
    data = request.json
    print(f"[Гриф] Принял: {data["message"]}")

    grif_log = {"source": "Гриф", "message": data["message"]}

    try:
        kollektiv_data = requests.post(KOLLEKTIV_URL, json=grif_log)
        print(f"[Гриф] Отправлено в Коллектив: {grif_log}", flush=True)
        return kollektiv_data.json(), kollektiv_data.status_code
    except requests.ConnectionError:
        print("[Гриф] Коллектив недоступен", flush=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)