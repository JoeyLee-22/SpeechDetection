import numpy as np
from math import ceil
from scipy.signal import butter,filtfilt
from scipy.io.wavfile import write

def make_white_noise(s, sample_rate):
    length_in_seconds = ceil(s.shape[0]/sample_rate)
    n = np.random.normal(-1, 1, sample_rate * length_in_seconds)
    
    cutoff = 10000
    nyq = sample_rate/2
    order = 5
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    n = filtfilt(b, a, n)
    
    return n