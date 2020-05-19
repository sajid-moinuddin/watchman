import os
import json
import logging
import sys
import pprint
import time
from pubsub import pub
from watchman.newrelic_insight import NewrelicInsight
from watchman.newrelic_event_channel import NewrelicEventsChannel, K8sEvent
from watchman.watchman_utils import Utils
# from watchman.vektor_newrelic_event_handler import VektorNewrelicEventHandler
from watchman.local_computer_newrelic_event_handler import LocalComputerEventHandler
import logging.handlers

def begin(log_level = logging.INFO):
    print('.............Night gathers, and now my watch begins..............\n')
    logPath = '/var/log/watchman'
    fileName = 'watchman'

    logging.basicConfig(
        level=log_level,
        # format="%(asctime)s [%(threadName)-12.12s] [%(module)s:%(filename)s:%(lineno)d] [%(funcName)s->%(levelname)-5.5s]  %(message)s",
        format="%(asctime)s",
        
        handlers=[
            logging.FileHandler("/var/log/watchman/watchman.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # connection_logger = logging.getLogger('requests')
    # connection_logger.setLevel(log_level)

    # connection_logger = logging.getLogger('connectionpool')
    # connection_logger.setLevel(log_level)


    use_anki = os.environ.get('USE_ANKI')
    logging.debug("-----------------")
    print("-------------------")

    # ------------------------------------------------------
    directory_path = os.path.dirname(__file__)

    print(directory_path)

    if use_anki == 'True':
        use_anki = True
    else:
        use_anki = False

    anki_serial = os.environ.get('ANKI_ROBOT_SERIAL')
    channel = NewrelicEventsChannel( os.environ.get('NEW_RELIC_ACCOUNT_ID_PROD'), os.environ.get('NEW_RELIC_INSIGHT_API_KEY'))

    # if use_anki :
    #     event_handler = VektorNewrelicEventHandler(anki_serial)
    #     event_handler.startListen()

    local_event_handler = LocalComputerEventHandler()
    local_event_handler.startListen()

    thread = channel.start(15)
    thread.join()
    