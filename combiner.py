import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from scipy import stats
from scipy.signal import butter,filtfilt
from scipy.io.wavfile import write
from scipy.io.wavfile import read

class Combiner():
    def __init__(self, filename, n_type):
        self.filename = filename
        
        # self.samplerate_s, self.s = read("audio/{}".format(filename))
        self.samplerate_s, self.s = read("audio/long_sentence.wav")
        self.s = np.array(self.s,dtype=float)[:250000]
        
        if (n_type=="white"):
            self.sample_rate = 44100
            self.length_in_seconds = ceil(self.s.shape[0]/self.sample_rate)
            self.n = np.random.normal(-1, 1, self.sample_rate * self.length_in_seconds)
            
            cutoff = 10000
            nyq = self.sample_rate/2
            order = 5
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            self.n = filtfilt(b, a, self.n)
            
            write('audio/whiteNoise.wav', self.sample_rate, self.n)

            self.s = np.append(self.s, [0]*(self.length_in_seconds*self.sample_rate - self.s.shape[0])) 
            write('audio/shortened_sentence.wav', self.samplerate_s, 0.0005*self.s)

        elif (n_type=="babble"):
            self.sample_rate, self.n = read("audio/babbleNoise.wav")
            self.n = np.array(self.n,dtype=float)[:self.s.shape[0]]

    def babble_combine(self, a):
        y = 0.0005*self.s+a*self.n
        write('audio/a*n.wav', self.sample_rate, a*self.n)
        write('audio/babble_combined.wav', self.samplerate_s, y)
        
    def white_combine(self, a):
        y = 0.0005*self.s+a*self.n
        write('audio/a*n.wav', self.sample_rate, a*self.n)
        write('audio/white_combined.wav', self.samplerate_s, y)