from deepgram import Deepgram
import asyncio, json, os

def test():
    dg_key = '7f065218f997c7ae17151100cb616c59a281a793'
    dg = Deepgram(dg_key)

    MIMETYPE = 'wav'

    DIRECTORY = 'audio'
    audio_file = 'combined.wav'

    options = {
        "punctuate": True,
        "model": 'general',
        "tier": 'enhanced'
    }

    with open(f"{DIRECTORY}/{audio_file}", "rb") as f:
        source = {"buffer": f, "mimetype":'audio/'+MIMETYPE}
        res = dg.transcription.sync_prerecorded(source, options)
        with open(f"./{audio_file[:-4]}.json", "w") as transcript:
            json.dump(res, transcript)

    OUTPUT = 'combined.json'

    with open(OUTPUT, "r") as file:
        data = json.load(file)
        result = data['results']['channels'][0]['alternatives'][0]['transcript']
        result = result.split('.')
        for sentence in result:
            return(sentence)