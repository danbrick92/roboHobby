import led
import json
import time

class led_song:
    
    directions = ""
    config_file = ""
    
    # Create an led show object
    def __init__(self,song_name):
        # Load config file
        self.get_led_song_fname(song_name)
        with open(self.config_file) as file:
            c = file.read()
            content = json.loads(c)
        self.config_file = content
        # Get directions from json
        self.set_directions()
    
    # Gets a song config file
    def get_led_song_fname(self,song):
        self.config_file = 'songs/' + song + '.json'
        
    # Set directions from config data
    def set_directions(self):
        self.directions = []
        list_of_dir = self.config_file['directions']
        fin = len(list_of_dir)
        last = 0
        for i in range(0,fin):
            d = list_of_dir[i]
            cur = float(list(d.keys())[0])
            w_time = cur-last
            new_dir = [w_time, list(d.values())[0] ]
            self.directions = self.directions + new_dir
            last = cur
        print("Directions set")
        
    # Play the led song from directions
    def play(self):
        for d in self.directions:
            if isinstance(d,str):
                for i in range(0,2):
                    if d == "hi":
                        led.hi()
                    elif d == "med":
                        led.med()
                    elif d == "low":
                        led.low()
                    elif d == "hi_fast":
                        led.hi_fast()
                    elif d == "hi_slow":
                        led.hi_slow()
            else:
                time.sleep(d)