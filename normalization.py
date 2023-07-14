from math import sqrt

def get_avg(y):
    tot = 0
    for num in y:
        tot += num
    return tot/len(y)

def rms(y):
    avg = get_avg(y)
    tot = 0
    for num in y:
        tot += (num - avg)**2
    return sqrt(tot/len(y))