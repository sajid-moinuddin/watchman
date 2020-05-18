from watchman.newrelic_insight import NewrelicInsight
from watchman.cache import Cache
from watchman.watchman_utils import Utils

from collections import OrderedDict 
import logging
import threading
import json
import time
import datetime
from dateutil import parser
from pubsub import pub


class K8sEvent:    
    def __init__(self, event):
        self.original_event = event
        self.cluster = event['clusterName']
        self.uuid = event['event.metadata.uid']
        self.event_type = event['event.type']
        self.occurrance_count = event['event.count']
        try:
            self.object_name = event['event.involvedObject.fieldPath'][16:len(event['event.involvedObject.fieldPath'])-1]
        except Exception as e:    
            self.object_name = event['event.involvedObject.name']            
        self.source = event['event.source.component']
        self.reason = event['event.reason']
        self.first_occurrance = self.convert_to_local_time(event['event.firstTimestamp'])
        self.last_occurrance = self.convert_to_local_time(event['event.lastTimestamp'])
        self.namespace = event['event.metadata.namespace']
        self.message = event['event.message']
        self.kind = event['event.involvedObject.kind']
    
    def cache_key(self):
        return f"{self.uuid}"        

    def convert_to_local_time(self, utc_time):
        dt_utc = parser.parse(utc_time)
        return dt_utc.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    def print_full(self):
        return json.dumps(self.original_event, indent=4)

    def __str__(self):
        return f" {self.event_type} [{self.cache_key()} :: {self.namespace}/{self.source}/{self.object_name} : {self.reason} [{self.first_occurrance}..{self.last_occurrance} ] [{self.message}]"

class NewrelicEventsChannel:
    nr_insight = None
    subscribers = {}
    processedEvents = {}
    stop_poll = False
    poll_frequency_seconds = 30
    cache = Cache(max_size=100)

    def __init__(self, account_id, api_key):
        self.nr_insight = NewrelicInsight(account_id, api_key)


    def on_new_event(self, the_event: K8sEvent):
        # logging.info("Firing new event: %s", the_event)
        pub.sendMessage('newrelic.kubernetes', event=the_event)

    def poll(self):
        logging.info("In the Poll Method!!")

        # Build History of existing event so It doesn't show in the future (its assumed existing events are already being looked after)
        events = self.nr_insight.get_events_not_normal('kubernetes', 100)
        init_events = self.find_new_events(events)
        for event in init_events:
            logging.debug("***** Existing Event: %s", event.print_full())
            Utils.append_to_logfile(event.print_full())
        logging.info("-----------------------------------------------------------------------------------------------------------------------")
        time.sleep(30)

        while self.stop_poll != True:
            try: 
                events = self.nr_insight.get_events_not_normal('kubernetes', 15)
                logging.debug("*******************************************: fetched %s events \n", len(events))

                new_events = self.find_new_events(events)
                if len(new_events) > 0:
                    for event in new_events: 
                        self.on_new_event(event)
                else:
                    logging.info("No new event in last %s seconds", self.poll_frequency_seconds)                        

            except Exception as e: 
                logging.exception("Exception")
            finally:
                time.sleep(self.poll_frequency_seconds)
                

    def start(self, poll_frequency_seconds = 30):
        logging.info("NewrelicEventsChannel: starting thread with frequency: %s", poll_frequency_seconds)
        thread = threading.Thread(target=self.poll)
        thread.daemon = True
        self.stop_poll = False
        self.poll_frequency_seconds = poll_frequency_seconds
        thread.start()
        logging.info("NewrelicEventsChannel    : after creating thread")
        return thread

    def stop(self):
        logging.warn("NewrelicEventsChannel    : stopping thread")
        self.stop_poll = True

    def find_new_events(self, events): 
        new_events = []
        for event in events: 
            k8s_event = K8sEvent(event)  
            if self.cache.set(k8s_event.cache_key(), k8s_event) == True:
                new_events.append(k8s_event)
        return new_events                              

    def convert_to_local_time(self, utc_time):
        dt_utc = parser.parse(utc_time)
        return dt_utc.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)