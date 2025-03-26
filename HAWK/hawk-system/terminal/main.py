import requests
import random
import time

time.sleep(10)

GRIF_URL = "http://grif:8001/process"
VETROLOV_URL = "http://vetrolov:8005/energy"

def command_event():
    while True:
        rand = random.randint(0, 20)
        if rand == 3:
            rand_ = bool(random.getrandbits(1))
            if rand_:
                command_data = {"message": "reboot" }
                response = requests.post(GRIF_URL, json=command_data)
        
                print(f"[Терминал управления] Приказ отправлен в Гриф: {command_data}", flush=True)
            else:
                command_data = {"message": "power_off" }
                response = requests.post(VETROLOV_URL, json=command_data)
        
                print(f"[Терминал управления] Приказ отправлен в Ветролов: {command_data}", flush=True)

        time.sleep(1)

if __name__ == "__main__":
    print("[Терминал управления] Начал работу", flush=True)
    command_event()