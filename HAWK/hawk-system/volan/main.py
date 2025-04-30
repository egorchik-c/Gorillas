from flask import Flask, request
import requests
import logging
import time

time.sleep(2)

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

GRIF_URL = "http://grif:8001/process"
REPAIR_URL = "http://repair:8003/fix"
SECURITY_URL = "http://security:8004/check"



@app.route("/motion", methods=["POST"])
def receive_motion():
    data = request.json
    print(f"[Волан] Принято от ромашки: {data}")

    message = data.get("status")

    if message == "access":
        print(f"[Волан] Доступ разрешен, отправляю в Гриф")
        send_to_grif(message)
    elif message == "denied":
        print(f"[Волан] Доступ запрещен, отправляю в Охрану")
        send_to_security(message)
    elif message == "repair":
        print(f"[Волан] Запрос на ремонт")
        send_to_repair(message)

    return {"status": "OK"}, 200

def send_to_grif(message):
    grif_data = requests.post(GRIF_URL, json={"source": "Волан", "message": message})
    log = grif_data.json()
    print(f"[Волан] Отправлено в гриф {message}", flush=True)
    return {"message": message}, 200

def send_to_security(message):
    sec_data = requests.post(SECURITY_URL, json=message)
    response = sec_data.json()
    print(f"[Волан] Ответ от Охраны: {response["status"]}", flush=True)
    send_to_grif(response["status"])

def send_to_repair(message):
    repair_data = requests.post(REPAIR_URL, json=message)
    response = repair_data.json()
    print(f"[Волан] Ответ от Ремонта: {response["status"]}", flush=True)
    send_to_grif(response["status"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)