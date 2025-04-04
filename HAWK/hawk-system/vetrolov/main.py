from flask import Flask, request
import requests
import logging
import time

time.sleep(5)

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

DIAG_URL = "http://diagnostic:8006/confirm"

@app.route("/energy", methods=["POST"])
def energy_event():
    data = request.json
    print(f"[Ветролов] Принял и отправил на диагностику: {data["message"]}", flush=True)
    diag_data = requests.post(DIAG_URL, json=data)
    response = diag_data.json()
    if response.get("status") == "Diagnostic OK": 
        print("[Ветролов] Отключил питание", flush=True)
    else:
        print("[Ветролов] Отключение не одобрено", flush=True)

    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8005)