import os
import _thread
import led_song

SONGS = [ "scctt" , "wwymc"]

def get_song_filename(song):
    return 'songs/' + song + '.wav'

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
    
for song in songs:
    do_show(song)