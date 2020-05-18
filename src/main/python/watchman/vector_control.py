import os
import time
import logging 
from concurrent.futures import wait

from watchman.text_to_image import make_text_image

import anki_vector
from anki_vector import AsyncRobot, behavior
from anki_vector.util import degrees
from anki_vector import util as anki_util

def make_scene(anki_serial, text):
    robot =  AsyncRobot(anki_serial)
    try:
        robot.connect()

        f='vector_alert.wav'
        robot.behavior.set_eye_color(1,1) #reddish
        robot.anim.play_animation('anim_eyepose_furious')
        logging.debug("play alert...")
        stream_future = robot.audio.stream_wav_file(f,50)
        robot.anim.play_animation('anim_communication_cantdothat_01')

        if robot.status.is_on_charger:
            print("Robot is in charger, lets drive off")
            drive_future = robot.behavior.drive_off_charger()
            drive_future.result()

        robot.behavior.say_text("ALERT!")
        r = robot.anim.play_animation('anim_communication_cantdothat_01')
        r.result()
        stream_future = robot.audio.stream_wav_file(f,50)
        stream_future.result()

        robot.behavior.say_text("ALERT!")
        r = robot.anim.play_animation('anim_communication_cantdothat_01')
        r.result()
        stream_future = robot.audio.stream_wav_file(f,50)
        stream_future.result()

        for i in range(1, 5):
            robot.behavior.set_head_angle(degrees(50.0))
            robot.behavior.set_lift_height(0.0)
            image = make_text_image(text, 0, 0)
            screen_data = anki_vector.screen.convert_image_to_screen_data(image)
            r = robot.screen.set_screen_with_image_data(screen_data, 5.0, interrupt_running=True)
            r.result()
            time.sleep(5)

        robot.behavior.say_text("I WARNED YOU!!!!")
        robot.behavior.set_head_angle(degrees(50.0))
        robot.behavior.set_lift_height(0.0)
        image = make_text_image("I WARNED YOU !!! \nI WARNED YOU !!!\nI WARNED YOU !!!", 0, 0)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image)
        r = robot.screen.set_screen_with_image_data(screen_data, 5.0, interrupt_running=True)
        r.result()
        time.sleep(5)

        robot.behavior.say_text("going back home...BYE BYE!")

        time.sleep(5)

        # time.sleep(20)
        for i in range(1, 5):
            if robot.status.is_on_charger is False:
                drive_future = robot.behavior.drive_on_charger()
                r = drive_future.result()
                logging.debug("Drive Back Home Result: %s", r)
                time.sleep(5)
    finally:
        try:
            robot.disconnect()
        except:
            print('Connection was not nicely cleaned!!!')        
        finally:
            print("....DONE....")       

def make_scene_light(anki_serial, text):
    robot =  AsyncRobot(anki_serial)
    try:
        robot.connect()
        f='vector_bell_whistle.wav'
        robot.behavior.set_eye_color(1,1) #reddish
        for i in range(1,3):
            stream_future = robot.audio.stream_wav_file(f,50)
            stream_future.result()
            time.sleep(1)
        robot.behavior.say_text("ALERT!")
        robot.behavior.set_head_angle(degrees(50.0))
        robot.behavior.set_lift_height(0.0)
        image = make_text_image(text, 0, 0)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image)
        for i in range(1, 10):
            r = robot.screen.set_screen_with_image_data(screen_data, 5.0, interrupt_running=True)
            r.result()
            time.sleep(3)
        for i in range(1, 5):
            if robot.status.is_on_charger is False:
                drive_future = robot.behavior.drive_on_charger()
                r = drive_future.result()
                logging.debug("Drive Back Home Result: %s", r)
                time.sleep(5)
    finally:
        try:
            robot.disconnect()
        except:
            print('Connection was not nicely cleaned!!!')        
        finally:
            print("....DONE....")                   


