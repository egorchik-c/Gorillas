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

    command = data.get("message")

    if command == "reboot":
        print(f"[Гриф] Перезаргрузка на 15 сек, ожидайте...", flush=True)
        time.sleep(15)
        print(f"[Гриф] Возобновление работы системы", flush=True)
    elif command == "Отключение питания Ветролова":
        print("[Гриф] Система без питаня", flush=True)
        
    kollektiv_data = requests.post(KOLLEKTIV_URL, json=data)
    print(f"[Гриф] Отправлено в Коллектив: {data["message"]}", flush=True)

    return kollektiv_data.json(), kollektiv_data.status_code
    # except requests.ConnectionError:
    #     print("[Гриф] Коллектив недоступен", flush=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)