import os
import json
import multiprocessing
import threading

from uuid  import uuid4
from confluent_kafka import Producer
from random import getrandbits
from time import sleep

MODULE_NAME: str = os.getenv("MODULE_NAME")
requests_queue: multiprocessing.Queue = None

def proceed_to_deliver(id, details):
    details["id"] = id
    details["source"] = MODULE_NAME
    requests_queue.put(details)

def producer_job(_, config, request_queue: multiprocessing.Queue):
    producer = Producer(config)

    # threading.Thread(target=get_telemetry).start()

    def delivery_callback(err, msg):
        if err:
            print(f"[{MODULE_NAME}] Message failed delivery: {err}")

    topic = "monitor"
    while True:
        event_details = request_queue.get()
        producer.produce(
            topic,
            json.dumps(event_details),
            event_details["id"],
            callback=delivery_callback
        )
        producer.poll(15000)
        producer.flush()
        print(f"[{MODULE_NAME}] Send collect data: {event_details}")

def start_producer(args, config, request_queue):
    print(f"[{MODULE_NAME}] Producer started...")

    global requests_queue

    requests_queue = request_queue

    threading.Thread(
        target=lambda: producer_job(args, config, request_queue)
    ).start()