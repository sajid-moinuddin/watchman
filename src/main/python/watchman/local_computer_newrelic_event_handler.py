from pubsub import pub
import logging
from watchman.watchman_utils import Utils
from watchman.newrelic_event_channel import NewrelicEventsChannel, K8sEvent
import anki_vector
from threading import Thread
from queue import Queue
import time
from anki_vector import Robot

class LocalComputerEventHandler:
    def on_new_event(self, event: K8sEvent):
        Utils.whistle(2)
        Utils.append_to_logfile(event.print_full())
        text_2_speech = f"{event.cluster} {event.event_type}! {event.reason} {event.kind}!, {event.object_name}!, namespace: {event.namespace}" 
        Utils.text_2_speech(text_2_speech)
        # Utils.text_2_speech(f"summary: {event.message}")
        logging.info("____>>>> %s", event.print_full())
        logging.info("____>>>> %s", event)
        logging.debug("---------------------------------------------------------------------------------------")
        
    def startListen(self):
        pub.subscribe(self.on_new_event, 'newrelic.kubernetes')

