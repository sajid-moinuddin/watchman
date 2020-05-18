from watchman.vector_control import make_scene
from watchman.vector_control import make_scene_light
from watchman.watchman_utils import Utils
from watchman.newrelic_event_channel import NewrelicEventsChannel, K8sEvent

from pubsub import pub
import logging
import anki_vector
from threading import Thread
from queue import Queue
import time
from anki_vector import Robot

class VektorNewrelicEventHandler:
    vektor_action_queue = Queue()
    robot = None

    def __init__(self, anki_serial):
        self.anki_serial = anki_serial

    def on_new_event(self, event: K8sEvent):
        logging.debug("____: New Event: %s", event)
        Utils.beep(1)
        if self.should_alert(event): 
            self.vektor_action_queue.put(event)

    def should_alert(self, event: K8sEvent):
        return True

    def vector_action(self, event: K8sEvent):
        logging.debug("******: ")


    def startListen(self):
        pub.subscribe(self.on_new_event, 'newrelic.kubernetes')
        t = Thread(target = self.poll_for_action) 
        t.daemon = True
        t.start()
        return t

    def poll_for_action(self):
        while True:
            try:
                event = self.vektor_action_queue.get()
                self.handle_event(event)            
                self.vektor_action_queue.task_done()
            finally:
                time.sleep(30) #dont overwhelm vector!!

    def handle_event(self, event: K8sEvent):
        logging.info("about to get vector to make a scene...: %s", event)
        txt = f"{event.event_type}\nns: {event.namespace}\n{event.source}:{event.occurrance_count}\n{event.object_name}\n{event.message}"
        make_scene_light(self.anki_serial, txt)
        logging.info("************************* DONE VECTOR ACTION***********************************")

    # def get_robot(self): 
    #     if self.robot is None:
    #         self.robot = Robot(self.anki_serial)
    #         self.robot.connect()

    #     return self.robot    

