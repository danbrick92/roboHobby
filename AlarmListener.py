"""
This program streams microphone input and listens for security system alarm.
In the case that it picks up the alarm, it will alert the sms receiver.

To Do:
-Breakout steps into functions
-Logic to trigger alarm state
  -Sleep timer of 1
  -Consecutive dB timer of 5 (within a period of 20 seconds)
  -Alarm state sleep timer of 1 hour
-Send SMS to person from SMS file
"""
import time
import math
import pyaudio
import wave
import sys
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt


ALARM_COUNT = 0

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

# This function records audio from the microphone
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
# Saves the recorded audio to a wav file
def save_wav():
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Analyze dB to match alarm sound levels
def analysis():
    [Fs, x] = audioBasicIO.readAudioFile("output.wav");
    F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 1.0000*Fs, 0.025*Fs);
    averageEnergy = sum(F[1,:])/len(F[1,:])
    if averageEnergy >= 1.5:
        ALARM_COUNT +=1

# Triggers alarm based on ALARM COUNT
def check_trigger_alarm():
    if ALARM_COUNT >= 3:
        trigger_alarm()
        
# Logic for what alarm trigger does
def trigger_alarm():
    ALARM_COUNT = 0
    send_sms("The security system alarm has been triggered")
    time.sleep(3600) # Sleep for an hour - don't want to be bombarded with texts
    
# Sends a text message to numbers from data file
def send_sms(message):
    return 0

def main():
    while True:
        #record_audio()
        #save_wav()
        analysis()
        check_trigger_alarm()
        time.sleep(2)
    
if __name__ == "__main__":
    main()