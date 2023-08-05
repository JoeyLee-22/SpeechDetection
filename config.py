import json

# config = {"demo_mode":False,
#           "is_logging":True,
#           "log_folder":"logV8",
#           "is_graphing":False,
#           "sentence_start_sec":9, 
#           "sentence_end_sec":13, 
#           "sweep_start":0, 
#           "sweep_end":10}

config = {"model_filename":"speech_detection_model3.joblib",
          "audio_filename":"logV7/07-16,17:08:26,a=6.40,SNR=0.02/s_prime.wav",
          "train":False,
          "load_and_predict":True}

with open('config.json', 'w') as f:
    json.dump(config, f)