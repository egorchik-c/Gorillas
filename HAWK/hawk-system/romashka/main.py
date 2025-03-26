import requests
import random
import time

time.sleep(1)

VOLAN_URL = "http://volan:8000/motion"

def detect_motion():
    while True:
        try:
            motion = bool(random.getrandbits(1))
            if motion:
                motion_data = {"motion_detected": motion, "status": random.choice(["repair", "denied", "access"])}
            else:
                motion_data = {"motion_detected": motion, "status": "access"}

            
            response = requests.post(VOLAN_URL, json=motion_data)
        
            print(f"[Ромашка] Успешно отправлено: {motion_data}", flush=True)
            time.sleep(25)

        except requests.ConnectionError:
            #print("[Ромашка]Ошибка подключения: Волан недоступен. Повтор через 5 сек.")
            time.sleep(5) 
        

if __name__ == "__main__":
    print("[Ромашка] Начала работу", flush=True)
    detect_motion()