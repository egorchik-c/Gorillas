from flask import Flask, request
import requests
import logging
import random
import time

time.sleep(1.5)


app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

@app.route("/check", methods=["POST"])
def check_event():
    data = request.json
    print(f"[Охранная система] Принято: {data}", flush=True)

    resolve_flag = bool(random.randbytes(1))

    if resolve_flag:
        print(f"[Охранная система] Оторвал Ване голову", flush=True)
    else:
        print(f"[Охранная система] Ситуация решена", flush=True)

    return {"status": "Охрана решила проблему"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004)
