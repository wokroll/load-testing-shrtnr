import numpy as np


def random_list_generator(list_length):
    mu, sigma = 3, 5 # mean and standard deviation
    randomList = list(abs(np.random.normal(mu, sigma, list_length)))
    randomList[3] = None
    return randomList
