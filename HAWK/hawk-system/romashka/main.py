import requests
import time
import random

VOLAN_URL = "http://volan:8000/motion"

def detect_motion():
    time.sleep(5)
    while True:
        try:
            motion_data = {"motion_detected": bool(random.getrandbits(1))}
            response = requests.post(VOLAN_URL, json=motion_data)
            
            if response.status_code == 200:
                print(f"[Ромашка] Успешно отправлено: {motion_data}", flush=True)
            else:
                print(f"[Ромашка] Ошибка обработки: {response.status_code}", flush=True)
            time.sleep(6)

        except requests.ConnectionError:
            print("[Ромашка]Ошибка подключения: Волан недоступен. Повтор через 5 сек.")
            time.sleep(5) 
        

if __name__ == "__main__":
    detect_motion()