from flask import Flask, request
import requests
import logging

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

KOLLEKTIV_URL = "http://kollektiv:8002/log"

@app.route("/process", methods=["POST"])
def process_event():
    data = request.json
    print(f"Гриф принял: {data["message"]}")

    grif_log = {"source": "Гриф", "message": f"{data["message"]}"}
    kollektiv_data = requests.post(KOLLEKTIV_URL, json=grif_log)
    print(f"Отправлено в Коллектив: {grif_log}", flush=True)

    return {"status": "SEND_TO_KOLLEKTIV"}, kollektiv_data.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)