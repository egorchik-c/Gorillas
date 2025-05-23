import os
import json
import threading

from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")

def send_telemetry(id, details):
    print("[DEBUG] Telemetry: ", details["telemetry"])
    validator(id, {"valid": details["telemetry"]})

def data_to_valid(id, details):
    print("[DEBUG] Data: ", details["data"])
    validator(id, {"mb_valid": details["data"]})

data_dict = {}

def validator(id, details):
    print("[{MODULE_NAME}] Our data: ", details)
    global data_dict

    if len(data_dict) > 2:
        data_dict = {}
    data_dict.update(details)
    print("TO-VALID = ", data_dict)

    if data_dict["valid"].get("motion_detected") == data_dict["mb_valid"].get("motion_detected"):
        print(f"[{MODULE_NAME}] Send data:", data_dict["mb_valid"])
        proceed_to_deliver(id, {
            "deliver_to": "validator",
            "operation": "send_to_cypher",
            "data": data_dict["mb_valid"]
        })
    else:
        print(f"[{MODULE_NAME}] ERROR: no valid video")
    

commands = {
    "data_to_valid": data_to_valid,
    "send_telemetry": send_telemetry
}

def handle_event(id, details_str):
    """ Обработчик входящих в модуль задач. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    # Выполнение нужной команды
    command = commands.get(operation)
    if command:
        command(id, details)

def consumer_job(args, config):
    consumer = Consumer(config)

    def reset_offset(verifier_consumer, partitions):
        if not args.reset:
            return

        for p in partitions:
            p.offset = OFFSET_BEGINNING
        verifier_consumer.assign(partitions)

    topic = MODULE_NAME
    consumer.subscribe([topic], on_assign=reset_offset)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    handle_event(id, details_str)
                except Exception as e:
                    print(f"[error] Malformed event received from " \
                          f"topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

def start_consumer(args, config):
    print(f'{MODULE_NAME}_consumer started')
    threading.Thread(target=lambda: consumer_job(args, config)).start()