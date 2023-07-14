from combiner import Combiner
from speechToText import recognize_from_file
from graphs import grapher
from deepgramAPI import test
import azure.cognitiveservices.speech as speechsdk

def call_combiner(combiner, n_type, a):
    if (n_type=="white"):
        combiner.white_combine(a)
    elif (n_type=="babble"):
        combiner.babble_combine(a)  
        
def get_alt_sentence(n_type):
    return recognize_from_file(speechsdk.audio.AudioConfig(filename=f"audio/{n_type}_combined.wav"))

def start(test_mode, graph, combine, a, sentence_filename, n_type):
    combiner = Combiner(sentence_filename, n_type)
    ogSentence = recognize_from_file(speechsdk.audio.AudioConfig(filename="audio/{}".format(sentence_filename)))
    counter = 0
    
    if (test_mode):
        while(True):
            a = float(input("Enter \"a\" value: "))
            
            call_combiner(combiner, n_type, a)
                
            altSentence_azure = get_alt_sentence(n_type)
            
            if (altSentence_azure==""):
                print("NO WORDS DETECTED\n")
            else:
                # print("Original Sentence: {}".format(ogSentence))
                print("Combined Sentence: {}\n".format(altSentence_azure))
    
    elif (combine):
        for i in range(1000):
            call_combiner(combiner, n_type, a)

            print("a: " + str(f'{a:.5f}'))
            altSentence_azure = get_alt_sentence(n_type)
            
            # if (altSentence_azure==""):
            #     print("NO WORDS DETECTED\n")
            #     break
            
            print("Original Sentence: {}".format(ogSentence))
            print("Combined Sentence: {}\n".format(altSentence_azure))
            
            if (n_type=="white"):
                a += 0.1
            elif (n_type=="babble"):
                a += 0.001
                
            if(graph):
                grapher(sentence_filename)
        
        # if (n_type=="white"):
        #     new_a = a+6
        #     print("GENERATING FINAL COMBINED AUDIO WITH a = {}\n".format(f'{new_a:.5f}'))
        #     combiner.white_combine(new_a)