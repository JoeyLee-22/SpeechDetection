import json

config = {"model_filename":"mfModel_1024hop.joblib",
          "audio_filename":"mfModelTrainingData2/rear_95db_a=9e-05.wav",
          "demo_mode":True,
          "predict":True,
          "train_model":False,
          "load_model":True,
          "save_model":False,
          "n_mfcc":13,
        #   "n_fft":2048,
          "n_fft":32768,
          "hop_length":32}

with open('config.json', 'w') as f:
    json.dump(config, f)