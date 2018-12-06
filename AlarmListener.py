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
import datetime
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

# This function records audio from the microphone
def record_audio():
    print("Will record " + str(RECORD_SECONDS) + " of audio")
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
    print("Saving audio to " + str(WAVE_OUTPUT_FILENAME))
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Analyze dB to match alarm sound levels
def analysis(alarm):
    print("Analyzing audio for alarm levels of loudness")
    [Fs, x] = audioBasicIO.readAudioFile("output.wav");
    F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 1.0000*Fs, 0.025*Fs);
    averageEnergy = sum(F[1,:])/len(F[1,:])
    if averageEnergy >= .15:
        alarm["count"] += 1
        print("Alarm loudness reached. Count is " + str(alarm["count"]))
    return alarm

# Triggers alarm based on ALARM COUNT
def check_trigger_alarm(alarm):
    print("Checking if alarm state is reached.")
    if alarm["count"] >= 3:
        print "Triggering alarm..."
        alarm = trigger_alarm(alarm)
    return alarm
        
# Logic for what alarm trigger does
def trigger_alarm(alarm):
    send_sms("The security system alarm has been triggered")
    alarm["count"] = 0
    print("Waiting for one hour")
    time.sleep(3600) # Sleep for an hour - don't want to be bombarded with texts
    return alarm
    
# Sends a text message to numbers from data file
def send_sms(message):
    return 0

def main():
    print("Starting loop")
    alarm = { "count" : 0, "last_triggered" : datetime.datetime.now()}
    while True:
        #record_audio()
        #save_wav()
        alarm = analysis(alarm)
        alarm = check_trigger_alarm(alarm)
        time.sleep(2)
    
if __name__ == "__main__":
    main()