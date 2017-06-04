#!/usr/bin/env python
import json
import logging
import threading
import time
import websocket


class WebsocketLoggingHandler(logging.StreamHandler):
    """
    A log handler class that sends logs to `sushibar_host` over WebSockets.
    """

    def on_message(self, ws, message):
        print('in on_message', 'no need to do anything for logging, but will need for commands...')
        # print('<<<<< received "' + message + ' from self.ws <<<<<')

    def on_error(self, ws, error):
        print('in on_error')
        print(error)

    def on_close(self, ws):
        print('in on_close')
        print("### closed ###")

    def __init__(self, sushibar_host="ws://127.0.0.1:8000/logs"):
        logging.StreamHandler.__init__(self)
        print("In WebsocketLoggingHandler __init__ method")
        self.ws = websocket.WebSocketApp(sushibar_host,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)
        print('starting ws.run_forever in a thread')
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def emit(self, record):
        # print(record.__dict__)
        # TODO: check if self.ws.sock.connected
        try:
            msg = self.format(record)
            # print('emitting', msg)
            self.ws.send(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print(record)
            self.handleError(record)



class JsonLoggingFormatter(logging.Formatter):
    """
    Format logging `LogRecord`s as JSON and add `chef_name` and `log_id` fields.
    """

    def __init__(self, chef_name=None, log_id=None):
        self.chef_name = chef_name
        self.log_id = log_id
        super(JsonLoggingFormatter, self).__init__()
 
    def format(self, record):
        data = record.__dict__
        if self.chef_name:
            data['chef_name'] = self.chef_name
        if self.log_id:
            data['log_id'] = self.log_id
        return json.dumps(data)



if __name__ == '__main__':
    print("REMOTE-LOGGING SUSHI CHEF STARTING UP *****************************")
    print("*******************************************************************")
    logger = logging.getLogger('sushi-chef-name')
    logger.setLevel(logging.DEBUG)
    # 
    # TODO: add local stdout + file logging handlers


    # STEP 1
    print()
    print("STEP 1: POST to /channels/9129138/runs/")
    print("Creates a new run and notifies sushibar that chef is starting")
    print("The sushibar server assigns and returns a unique identifier `log_id` for the logs of this run")
    log_id = 'thelogid29121fe' # = a unique identifier for the logs of a particular channel run


    # STEP 2
    print()
    print("STEP 2: wireup up the websocket logging handler for `log_id` run")
    websocket_handler = WebsocketLoggingHandler(sushibar_host="ws://127.0.0.1:8000/logs")
    json_formatter = JsonLoggingFormatter(chef_name='some-sushi-chef', log_id=log_id)
    websocket_handler.setFormatter(json_formatter)
    logger.addHandler(websocket_handler)
    time.sleep(0.1)       # without this wait, self.ws.sock is None 


    # STEP 3
    print()
    print("STEP 3: run the usual shushi chef logic")
    # MAIN APPLICATION #########################################################
    logger.info('Testing some info message')

    for i in range(3):
        logger.info('remaining %d seconds', i)
        time.sleep(1)

    logger.info('another info msg yo')
    # /MAIN APPLICATION ########################################################


    # STEP 4
    print()
    print("STEP 4: POST  /channels/9129138/runs/{{run_id}}/done/")
    print("This notifies the sushibar server that chef run is done.")
    # wait a little so any remaining responses come back...
    time.sleep(2)
    websocket_handler.ws.close()
    time.sleep(0.1)       # without this wait, the main thread exits too fast
                          # and we don't get to see the printouts from `on_close`

    print("*******************************************************************")
    print("************************************ REMOTE-LOGGING SUSHI CHEF DONE")
    print()


