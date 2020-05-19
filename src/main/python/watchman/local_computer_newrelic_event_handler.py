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
        pi_display_txt = f"{event.cluster} \nnamespace: {event.namespace}\n{event.event_type}! \n{event.reason} {event.kind}!, \n{event.object_name}! \nsummary: {event.message}"
        # Utils.text_2_speech(f"summary: {event.message}")
        logging.info("____>>>> %s", event.print_full())
        logging.info("____>>>> \n\n%s", pi_display_txt)
        logging.debug("------------------")
        
    def startListen(self):
        pub.subscribe(self.on_new_event, 'newrelic.kubernetes')

