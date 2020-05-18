import os
import logging
import simpleaudio as sa
from time import time, ctime
from gtts import gTTS

class Utils:
    @staticmethod
    def beep(count = 1):
        # b = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
        # b(count)
        logging.debug("Beep!")

    def append_to_logfile(txt):
        f=open("k8s_events.log", "a+")
        f.write(txt)
        f.write(f"\n-----------------------------------------{ctime(time())}----------------------------------------------------\n")
        f.close()

    @staticmethod
    def alarm(count = 1):
        for i in range(1, count + 1):
            directory_path = os.path.dirname(__file__)
            file_path = os.path.join(directory_path, 'vector_alert.wav')
            Utils.playfile(file_path)

    @staticmethod
    def whistle(count = 1):
        directory_path = os.path.dirname(__file__)
        file_path = os.path.join(directory_path, 'vector_bell_whistle.wav')
        for i in range(1, count + 1):
            Utils.playfile(file_path)


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




