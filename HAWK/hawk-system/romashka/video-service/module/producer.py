import os
import json
import configparser
from confluent_kafka import Producer

class VideoProducer:
    def __init__(self, config_path='./shared/config.ini' ):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.conf = {
            'bootstrap.servers': config.get("default", "bootstrap.servers"),
            # 'auto.offset.reset': config.get("default", "auto.offset.reset")
        }

        self.producer = Producer(self.conf)
        self.topic = 'video'
    
    def delivery_report(self, err, msg):
        if err:
            print("[error] Message failed delivery: {}".format(err))

    def send_video(self, video_data):
        try:
            self.producer.produce(
                topic=self.topic,
                value=json.dumps(video_data),
                callback=self.delivery_report
            )
            self.producer.flush()
            print(f"[Video-service] Sent video: {video_data}")
            
        except Exception as e:
            print(f"[Video-service] Error sending video: {e}")
        

