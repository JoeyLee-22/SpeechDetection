import os
import numpy as np
import string

def get_data():
    directory = 'log'

    file_to_delete = open("data.txt",'w')
    file_to_delete.close()

    file = open("data.txt", "a")
    for folder in os.listdir(directory):
        for filename in os.listdir(f'{directory}/{folder}'):
            file_path = os.path.join(f'{directory}/{folder}', filename)
            if (filename=='results.txt'):
                results = open(file_path, "r").read()
                line = results.split("\n")
                line[2] = line[2].lower().translate(str.maketrans('', '', string.punctuation))
                line[3] = line[3].lower().translate(str.maketrans('', '', string.punctuation))
                file.write(str(line) + '\n')
    file.close()

    file = open("data.txt", "r")
    lines = file.readlines()
    
    a = []
    snr = []
    S1 = []
    S1_prime = []
    scores = []
    
    for line in lines:
        vars = line.split(",")

        a.append(float(vars[0][2:len(vars[0])-1]))
        snr.append(vars[1][2:len(vars[1])-1])
        S1.append(vars[2][2:len(vars[2])-1])
        S1_prime.append(vars[3][2:len(vars[3])-3])
        scores.append(float(vars[4][2:len(vars[4])-3]))
        
        for i in range(len(snr)):
            try:
                snr[i] = float(snr[i])
            except:
                pass
                snr[i] = -10       

    return a, snr, S1, S1_prime, scores