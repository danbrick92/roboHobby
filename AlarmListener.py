"""
This program streams microphone input and listens for security system alarm.
In the case that it picks up the alarm, it will alert the sms receiver.
"""

import time
import math
import pyaudio
import wave
import sys
import datetime
import numpy as np
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import smtplib
import ssl
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
LOG_FILE = 'notableEvents.log'
BACKOUT_PERIOD = 60 # in seconds

# This function checks if the previous alarm was triggered past the backout period
def check_alarm_decrement(alarm):
    if alarm['count'] > 0:
        print("Checking if alarm is older than " + str(BACKOUT_PERIOD) + " seconds old")
        now = datetime.datetime.now()
        limit = now - datetime.timedelta(seconds=BACKOUT_PERIOD)
        then = alarm['last_triggered']
        if limit > then:
            alarm['count'] -= 1
            print("Alarm was triggered more than the backout period. Decrementing to " + str(alarm['count']))
    return alarm    

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
    return p,frames
    
# Saves the recorded audio to a wav file
def save_wav(p,frames):
    print("Saving audio to " + str(WAVE_OUTPUT_FILENAME))
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Analyze dB to match alarm sound levels
def analysis(alarm):
    print("Analyzing audio for alarm pitch")
    frequencies = list() # ME
    chunk = CHUNK
    # open up a wave
    wf = wave.open('output.wav', 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)
    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    while len(data) == chunk*swidth:
        # write data out to the audio stream
        stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/chunk
            frequencies.append(thefreq)
            #print "The freq is %f Hz." % (thefreq)
        else:
            thefreq = which*RATE/chunk
            frequencies.append(thefreq)
            #print "The freq is %f Hz." % (thefreq)
        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
    stream.close()
    p.terminate()

    # Check to trigger
    maxPitch = max(frequencies)
    print("Pitch Max=" + str(maxPitch))

    if maxPitch > 3300 and maxPitch < 3340:
        print(str(maxPitch))
        alarm["count"] += 1
        alarm['last_triggered'] = datetime.datetime.now()
        print("Time is " + str(alarm['last_triggered']))
        print("Alarm loudness reached. Count is " + str(alarm["count"]))
        log(maxPitch,alarm['last_triggered'])
    return alarm

# Triggers alarm based on ALARM COUNT
def check_trigger_alarm(alarm):
    print("Checking if alarm state is reached.")
    if alarm["count"] >= 1:
        print "Triggering alarm..."
        alarm = trigger_alarm(alarm)
    return alarm
        
# Logic for what alarm trigger does
def trigger_alarm(alarm):
    send_email("The security system alarm has been triggered")
    alarm["count"] = 0
    print("Waiting for one hour")
    time.sleep(3600) # Sleep for an hour - don't want to be bombarded with texts
    return alarm
    
# Sends an email message to addresses from data file
def send_email(message):
    s1,s1p,r1,r2 = get_sending_data()
    
    msg = MIMEMultipart()
    msg['From'] = s1
    msg['To'] = r1
    msg['Subject'] = "Alarm Triggered"
    msg.attach(MIMEText(message, 'plain'))
    attachment = open(WAVE_OUTPUT_FILENAME, "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % WAVE_OUTPUT_FILENAME)
    msg.attach(part)
    
    port = 465
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", port)
    server.login(s1, s1p)
    text = msg.as_string()
    server.sendmail(s1, r1, text)
    #server.sendmail(s1, r2, message)
    server.quit()

# Gets data file and returns values
def get_sending_data():
    with open('/home/pi/Programming/alarmdata.csv') as data_file:
        content = data_file.read()
    content = content.splitlines()
    contents = content[1].split(',')
    return contents[0],contents[1],contents[2],contents[3]

# Log any important events
def log(average_volume,timestamp):
    message = str(timestamp) + "  -  Volume: " + str(average_volume)
    with open(LOG_FILE,'a+') as log_file:
        log_file.write(message)
    
def main():
    print("Starting loop")
    alarm = { "count" : 0, "last_triggered" : datetime.datetime.now()}
    while True:
        alarm = check_alarm_decrement(alarm)
        audio,frames = record_audio()
        save_wav(audio,frames)
        alarm = analysis(alarm)
        alarm = check_trigger_alarm(alarm)
        time.sleep(2)
    
if __name__ == "__main__":
    main()