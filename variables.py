import numpy as np
from math import e,log,sqrt

def exponential_distribution(_lambda):
    u = np.random.uniform(0, 1)
    return -(1 / _lambda) * log(u, e)


def normal_distribution(mu, sigma):
    var1 = var2= 0
    
    while var2 <= (((var1 - 1) ** 2) / 2):
        var1 = exponential_distribution(1)
        var2 = exponential_distribution(1)
    u = np.random.uniform(0, 1)
    
    ret = var1 if u > 0.5 else -var1
    return ret * sqrt(sigma) + mu

def poisson_distribution(_lambda):
    n = 0
    u = np.random.uniform(0, 1)
    while u >= e ** (-_lambda):
        u_i = np.random.uniform(0, 1)
        u *= u_i
        n += 1
    return n

