from .producer import VideoProducer
import random
from time import sleep

def main():
    print("[Video-service] Started...")

    producer = VideoProducer()
   
    while True:
        sample_video = {
            "motion_detected": bool(random.getrandbits(1)),
            "format": "mp4"
        }
        producer.send_video(sample_video)