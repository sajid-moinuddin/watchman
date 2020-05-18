import anki_vector
from anki_vector import AsyncRobot, behavior
import os
import logging 
from concurrent.futures import wait
from anki_vector import util as anki_util
import time

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

anki_serial = os.environ.get('ANKI_ROBOT_SERIAL')

robot = AsyncRobot(anki_serial)

robot.connect()



