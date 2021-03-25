import time
import logging

from utils import (
    up_micronaut,
    down_micronaut,
    clean_db
)
from cannon import  Cannon


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
URL = "http://localhost:8080"

if __name__ == '__main__':
    cannon = Cannon(URL)
    cannon.start_shoot(qps=30, duration=30)
