#!/usr/bin/env python3
"""
Proof of concept of a logging Handler-type of object that sends over a WebSocket.
The `WebsocketLogger` run in a separate thread.
"""
import threading
import time
import websocket


class WebsocketLogger(object):

    def on_message(self, ws, message):
        print('in on_message')
        print('<<<<< received "' + message + ' from self.ws <<<<<')

    def on_error(self, ws, error):
        print('in on_error')
        print(error)

    def on_close(self, ws):
        print('in on_close')
        print("### closed ###")

    def __init__(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)

    def info(self, msg):
        print('in logger.info')
        print('>>>>> sending "' + msg + '" over self.ws >>>>>')
        self.ws.send(msg)



if __name__ == "__main__":
    # websocket.enableTrace(True)     # useful to see raw socket data being sent
    
    print('creating logger')
    logger = WebsocketLogger("ws://127.0.0.1:8000/chat") # should be /logs not /chat
    print('logger created')
    
    print('starting logger.ws.run_forever in a thread')
    wst = threading.Thread(target=logger.ws.run_forever)
    wst.daemon = True
    wst.start()

    time.sleep(0.1)       # without this wait, self.ws.sock is None 
    
    print('trying to log smth.')
    logger.info('This is an info message sent over WebSockets')
    logger.info('This is another info message sent over WebSockets')
    
    
    
    # wait a little so any remaining responses come back...
    time.sleep(2)
    # done
    logger.ws.close()
    time.sleep(0.1)       # without this wait, the main thread exits too fast
                          # and we don't get to see the printouts from `on_close`

