import requests
import random
import time

time.sleep(1)

VOLAN_URL = "http://volan:8000/motion"

def detect_motion():
    while True:
        try:
            motion_data = {"motion_detected": bool(random.getrandbits(1)), "status": random.choice(["repair", "denied", "access"])}
            response = requests.post(VOLAN_URL, json=motion_data)
        
            print(f"[Ромашка] Успешно отправлено: {motion_data}", flush=True)
            time.sleep(20)

        except requests.ConnectionError:
            #print("[Ромашка]Ошибка подключения: Волан недоступен. Повтор через 5 сек.")
            time.sleep(5) 
        

if __name__ == "__main__":
    detect_motion()