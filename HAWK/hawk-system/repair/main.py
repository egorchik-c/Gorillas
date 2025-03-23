from flask import Flask, request
import requests
import logging
import time

time.sleep(1.5)

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

#GRIF_URL = "http://volan:8000/motion"

@app.route("/fix", methods=["POST"])
def fix():
    data = request.json
    print(f"[Ремонтная система] Принято: {data}", flush=True)

    print(f"[Ремонтная система] Ремонт завершен", flush=True)

    return {"status": "Ремонт готов"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)