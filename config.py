import json

config = {"demo_mode":True,
          "is_logging":True, 
          "is_graphing":False,
          "sentence_start_sec":10, 
          "sentence_end_sec":14, 
          "sweep_start":0, 
          "sweep_end":10}

with open('config.json', 'w') as f:
    json.dump(config, f)