"""
This program streams microphone input and listens for security system alarm.
In the case that it picks up the alarm, it will alert the sms receiver.

To Do:
-Fix up ugly sounding audio
-Logic to track dB
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

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def main():
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
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()



if __name__ == "__main__":
    main()