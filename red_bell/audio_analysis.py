import pyAudioAnalysis
import pyaudio
import numpy as np
import wave
import librosa

song_names = [ "scctt" , "wwymc"]

# Analyze dB to match alarm sound levels
def analysis(song_name):
    # Generate the file name
    filename = "songs/{}.wav".format(song_name)
    print("Analyzing {}".format(filename))
    audio, sample_rate = librosa.load(filename)
    # open usp a wave
    try:
        wf = wave.open(filename, 'rb')
        
        print( "Number of channels",wf.getnchannels())
        print ( "Sample width",wf.getsampwidth())
        print ( "Frame rate.",wf.getframerate())
        print ("Number of frames",wf.getnframes())
        print ( "parameters:",wf.getparams())
    except Exception as e:
        print(e)
    finally:
        wf.close()

analysis(song_names[0])