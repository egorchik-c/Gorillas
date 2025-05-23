import os

from multiprocessing import Queue
from configparser import ConfigParser
from argparse import ArgumentParser, FileType
from time import sleep
from .producer import start_producer

# CONFIG_PATH: str = "./shared/config.ini"
MODULE_NAME: str = os.getenv("MODULE_NAME")

def main():
    print("[Video-service] Started...")

    parser = ArgumentParser()
    parser.add_argument("config_file", type=FileType("r"))
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser["default"])
    config.update(config_parser[MODULE_NAME])

    request_queue = Queue()
    print(f"Running: {MODULE_NAME} producer...")
    start_producer(args, config, request_queue)

    

