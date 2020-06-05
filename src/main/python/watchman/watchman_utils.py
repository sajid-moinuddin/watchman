import os
import logging
import simpleaudio as sa
from time import time, ctime
from gtts import gTTS
from os import system, name 


class Utils:
    @staticmethod
    def beep(count = 1):
        # b = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
        # b(count)
        logging.debug("Beep!")

    @staticmethod
    def clear():
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear')     

    @staticmethod
    def print_preety(dict_object, *argv):
        pattern = ''
        vars = []

        iter_arg = iter(argv)
        
        pattern += '{:70.62}'
        vars.append(dict_object[next(iter_arg)])

        for a in iter_arg:
            pattern += '{:20.16}'
            vars.append(str(dict_object[a]))

        print(pattern.format(*vars))

    def append_to_logfile(txt):
        f=open("/var/log/watchman/k8s_events.log", "a+")
        f.write(txt)
        f.write(f"\n-----------------------------------------{ctime(time())}----------------------------------------------------\n")
        f.close()

    @staticmethod
    def alarm(count = 1):
        for i in range(1, count + 1):
            Utils.playfile('/usr/local/share/vector_alert.wav')

    @staticmethod
    def whistle(count = 1):
        for i in range(1, count + 1):
            Utils.playfile('/usr/local/share/vector_bell_whistle.wav')


    @staticmethod
    def playfile(filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing

    @staticmethod
    def text_2_speech(*texts):
        language = 'en'
        for text in texts:
            logging.debug("--------------: Playing: [%s]", text)
            myobj = gTTS(text=text, lang=language, slow=False)
            myobj.save("/tmp/t2s.mp3")
            os.system("mpg321 /tmp/t2s.mp3")

    @staticmethod
    def parse_key_val(param):
        if param is None:
            return ()
        _split = param.split('=')
        return (_split[0], _split[1])


