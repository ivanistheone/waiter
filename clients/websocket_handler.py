#!/usr/bin/env python
import datetime
import json
import logging
import time

import threading
import websocket


# via https://stackoverflow.com/questions/3118059/how-to-write-custom-python-logging-handler
class WebsocketLoggingHandler(logging.StreamHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """

    def on_message(self, ws, message):
        print('in on_message')
        print('<<<<< received "' + message + ' from self.ws <<<<<')

    def on_error(self, ws, error):
        print('in on_error')
        print(error)

    def on_close(self, ws):
        print('in on_close')
        print("### closed ###")

    def __init__(self):
        logging.StreamHandler.__init__(self)
        print("In WebsocketLoggingHandler __init__ method")
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:8000/logs",
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)
        print('starting ws.run_forever in a thread')
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def emit(self, record):
        # print(record.__dict__)
        try:
            msg = self.format(record)
            self.ws.send(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print(record)
            self.handleError(record)




class JsonLoggingFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name
        super(JsonLoggingFormatter, self).__init__()
 
    def format(self, record):
        data = record.__dict__
        if self.task_name:
            data['task_name_from_formatter'] = self.task_name
        return json.dumps(data)


if __name__ == '__main__':
    logger = logging.getLogger('sushi-chef-name')
    logger.setLevel(logging.DEBUG)
    websocket_handler = WebsocketLoggingHandler()
    json_formatter = JsonLoggingFormatter(task_name='some task name')
    websocket_handler.setFormatter(json_formatter)

    logger.addHandler(websocket_handler)

    time.sleep(0.1)       # without this wait, self.ws.sock is None 



    # MAIN APPLICATION #########################################################

    logger.info('Testing some info message')

    for i in range(3):
        logger.info('remaining %d seconds', i)
        time.sleep(1)

    
    logger.info('another info msg yo')

    # /MAIN APPLICATION ########################################################





    # wait a little so any remaining responses come back...
    time.sleep(2)
    websocket_handler.ws.close()
    time.sleep(0.1)       # without this wait, the main thread exits too fast
                          # and we don't get to see the printouts from `on_close`



