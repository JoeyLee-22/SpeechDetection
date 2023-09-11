import os
import numpy as np
from wavImEx import import_wave_file, export_wave_file

def getPIDataArr(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        for line in file:
            numbers = [int(x) for x in line.strip().split()]
            data_list.append(numbers)
    return np.array(data_list)

def getSaveCuts(file, row, type):
    p1 = file[15*44024:30*44024]
    p2 = file[38*44024:53*44024]
    p3 = file[62*44024:77*44024]
    p4 = file[85*44024:100*44024]
    p5 = file[108*44024:124*44024]
    p6 = file[132*44024:148*44024]
    
    export_wave_file(f'mfModelTrainingData2/{type}_70db_a={row}e-05.wav', p1, 44100)
    export_wave_file(f'mfModelTrainingData2/{type}_75db_a={row}e-05.wav', p2, 44100)
    export_wave_file(f'mfModelTrainingData2/{type}_80db_a={row}e-05.wav', p3, 44100)
    export_wave_file(f'mfModelTrainingData2/{type}_85db_a={row}e-05.wav', p4, 44100)
    export_wave_file(f'mfModelTrainingData2/{type}_90db_a={row}e-05.wav', p5, 44100)
    export_wave_file(f'mfModelTrainingData2/{type}_95db_a={row}e-05.wav', p6, 44100)

def cutWaveFiles(data_array, path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            curr_path = os.path.join(subdir, file)
            row = int(curr_path[30])
            if (file == "bottom.wav"):
                bottom = import_wave_file(curr_path)
                getSaveCuts(bottom, row, 'bottom')
            elif (file == "front.wav"):
                front = import_wave_file(curr_path)
                getSaveCuts(front, row, 'front')
            elif (file == "rear.wav"):
                rear = import_wave_file(curr_path)
                getSaveCuts(rear, row, 'rear')
            
data_array = getPIDataArr('PIData.txt')
cutWaveFiles(data_array, "differentWhiteNoiseCombined")