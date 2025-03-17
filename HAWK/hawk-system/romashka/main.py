import requests
import time
import random

VOLAN_URL = "http://volan:8000/motion"

def detect_motion():
    while True:
        try:
            motion_data = {"motion_detected": bool(random.getrandbits(1))}
            response = requests.post(VOLAN_URL, json=motion_data)
            print(f"[Ромашка] Отправлено: {motion_data}", flush=True)
            time.sleep(3)
        except requests.ConnectionError:
            print("[Ромашка]Ошибка подключения: Волан недоступен. Повтор через 5 сек.")
            time.sleep(5)
            continue 
        

if __name__ == "__main__":
    detect_motion()