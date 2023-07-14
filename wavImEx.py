import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read

def import_wave_file(path):
    samplerate, y = read(path)
    return np.array(y,dtype=float)

def export_wave_file(path, y, sample_rate):
    write(path, sample_rate, y)