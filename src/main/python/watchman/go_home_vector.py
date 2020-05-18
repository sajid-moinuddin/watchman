import anki_vector
from anki_vector import Robot
import os
import logging 
from concurrent.futures import wait
import time

anki_serial = os.environ.get('ANKI_ROBOT_SERIAL')

robot = Robot(anki_serial)

try:
    robot.connect()
    if robot.status.is_on_charger:
        print("Robot is in charger do nothing")
    else:
        robot.behavior.say_text("going back home...bye bye!")
        robot.behavior.drive_on_charger()
finally:
    robot.disconnect()

