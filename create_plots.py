import matplotlib.pyplot as plt
from calc_percentile import calculate_percentile

duration = 30
max_qps = 100
latency_list = []

df = calculate_percentile(duration, max_qps, latency_list)

df.plot(x ="QPS(queries per second)", y="Latency, 50%", kind = 'line')
df.plot(x ="QPS(queries per second)", y="Latency, 90%", kind = 'line')
df.plot(x ="QPS(queries per second)", y="Latency, 99%", kind = 'line')
plt.show()