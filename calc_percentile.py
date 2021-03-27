import pandas as pd
from cannon import Cannon

def calc_percentile(percentile, latency_list):
    latency_list = list(filter(lambda x: x is not None, latency_list))
    select = percentile * len(latency_list)
    return sorted(latency_list)[int(select)]


def create_dataframe():
    return pd.DataFrame(columns=["Duration", "Queries sent", "QPS(queries per second)",
                                 "Latency, 50%", "Latency, 90%", "Latency, 99%", "Error rate"])


def calculate_percentile(duration, max_qps, cannon: Cannon):
    df = create_dataframe()
    for i in range(100, max_qps, 10):
        latency_list = cannon.start_shoot(max_qps, duration, threads=int(max_qps / 10))
        df.loc[i] = [duration,
                     duration*(i+1),
                     i+1,
                     calc_percentile(.5, latency_list),
                     calc_percentile(.9, latency_list),
                     calc_percentile(.99, latency_list),
                     100*latency_list.count(None)/len(latency_list)]
    return df
