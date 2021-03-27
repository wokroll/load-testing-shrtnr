import logging

from cannon import Cannon


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
URL = "http://localhost:8080"

if __name__ == '__main__':
    cannon = Cannon(URL)
    latencies = cannon.start_shoot(qps=100, duration=15, threads=80)
    print(latencies)
