import os
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from scipy import stats
from scipy.signal import butter,filtfilt
from scipy.io.wavfile import write
from scipy.io.wavfile import read


class Combiner():
    def __init__(self):
        self.s = read("audio/89wpm P&I - Start Beacon -15s - 70.75.80.85.90.95 with 10s gaps copy.wav")[1]*0.0005

        self.boerboel = read("whiteNoise/Boerboel - Bottom - PMax Masking.wav")[1]
        self.bottom = read("whiteNoise/SC2.3 - Bottom Channel.wav")[1]
        self.front = read("whiteNoise/SC2.3 - Front Channel.wav")[1]
        self.rear = read("whiteNoise/SC2.3 - Rear Channel.wav")[1]

        self.samplerate = 44100
        
        for i in range(4):
            self.boerboel = np.append(self.boerboel, self.boerboel)
            self.bottom = np.append(self.bottom, self.bottom)
            self.front = np.append(self.front, self.front)
            self.rear = np.append(self.rear, self.rear)
            
        self.boerboel = self.boerboel[:len(self.s)]
        self.bottom = self.bottom[:len(self.s)]
        self.front = self.front[:len(self.s)]
        self.rear = self.rear[:len(self.s)]

    def combine(self, a):
        newpath = f'differentWhiteNoiseCombined/a={a}'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        
        y1 = self.s + a*self.boerboel
        y2 = self.s + a*self.bottom
        y3 = self.s + a*self.front
        y4 = self.s + a*self.rear

        write(f'differentWhiteNoiseCombined/a={a}/boerboel.wav', self.samplerate, y1)
        write(f'differentWhiteNoiseCombined/a={a}/bottom.wav', self.samplerate, y2)
        write(f'differentWhiteNoiseCombined/a={a}/front.wav', self.samplerate, y3)
        write(f'differentWhiteNoiseCombined/a={a}/rear.wav', self.samplerate, y4)

obj = Combiner()
for i in range (10):
    obj.combine(round(0.00001*i,5))

# class Combiner():
#     def __init__(self, filename, n_type):
#         self.filename = filename
        
#         # self.samplerate_s, self.s = read("audio/{}".format(filename))
#         self.samplerate_s, self.s = read("audio/long_sentence.wav")
#         self.s = np.array(self.s,dtype=float)[:250000]
        
#         if (n_type=="white"):
#             self.sample_rate = 44100
#             self.length_in_seconds = ceil(self.s.shape[0]/self.sample_rate)
#             self.n = np.random.normal(-1, 1, self.sample_rate * self.length_in_seconds)
            
#             cutoff = 10000
#             nyq = self.sample_rate/2
#             order = 5
#             normal_cutoff = cutoff / nyq
#             b, a = butter(order, normal_cutoff, btype='low', analog=False)
#             self.n = filtfilt(b, a, self.n)
            
#             write('audio/whiteNoise.wav', self.sample_rate, self.n)

#             self.s = np.append(self.s, [0]*(self.length_in_seconds*self.sample_rate - self.s.shape[0])) 
#             write('audio/shortened_sentence.wav', self.samplerate_s, 0.0005*self.s)

#         elif (n_type=="babble"):
#             self.sample_rate, self.n = read("audio/babbleNoise.wav")
#             self.n = np.array(self.n,dtype=float)[:self.s.shape[0]]

#     def babble_combine(self, a):
#         y = 0.0005*self.s+a*self.n
#         write('audio/a*n.wav', self.sample_rate, a*self.n)
#         write('audio/babble_combined.wav', self.samplerate_s, y)
        
#     def white_combine(self, a):
#         y = 0.0005*self.s+a*self.n
#         write('audio/a*n.wav', self.sample_rate, a*self.n)
#         write('audio/white_combined.wav', self.samplerate_s, y)