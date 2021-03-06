import matplotlib.pyplot as plt
from calc_percentile import calculate_percentile
import logging

from cannon import Cannon
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
URL = "http://localhost:8080"

if __name__ == '__main__':
    cannon = Cannon(URL)

    duration = 30
    max_qps = 300

    df = calculate_percentile(duration, max_qps, cannon)

    df.plot(x ="QPS(queries per second)", y="Latency, 50%", kind = 'line')
    df.plot(x ="QPS(queries per second)", y="Latency, 90%", kind = 'line')
    df.plot(x ="QPS(queries per second)", y="Latency, 99%", kind = 'line')
    df.plot(x ="QPS(queries per second)", y="Error rate", kind = 'line')
    plt.show()