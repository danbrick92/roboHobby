import os
import _thread
import led_song
import switch
import time

SONGS = [ "scctt", "wwymc", "rrr", "jb"]

def get_song_filename(song):
    return '/home/pi/Programmer/roboHobby/red_bell/songs/' + song + '.wav'

def play(file):
    os.system("aplay " + file)
    
def light_show(led_song):
    led_song.play()

def do_show(song):
    # Create led song object
    ls = led_song.led_song(song)
    fname = get_song_filename(song)
    # Begin show
    _thread.start_new_thread( play, (fname,) )
    _thread.start_new_thread( light_show, (ls ,) )
    # Sleep
    sleep_time = 11
    if song == 'rrr':
        sleep_time = 9
    if song == 'jb':
        sleep_time = 7
    time.sleep(sleep_time) # Sleep for max song length
    

while True:
    is_on = switch.check_if_on()
    if is_on:
        for song in SONGS:
            do_show(song)
    else:
        time.sleep(5)
    
