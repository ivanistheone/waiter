#!/usr/bin/env python
# via https://stackoverflow.com/questions/29145442/threaded-non-blocking-websocket-client
import websocket
import threading
from time import sleep

def on_message(ws, message):
    print('in on_message')
    print(message)

def on_close(ws):
    print('in on_close')
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/chat",
                                on_message = on_message,
                                on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
        sleep(1)
        conn_timeout -= 1

    msg_counter = 0
    max_count = 2
    while ws.sock.connected:
        ws.send('Hello world %d'%msg_counter)
        sleep(1)
        msg_counter += 1
        if msg_counter > max_count:
            ws.sock.close()
            sleep(0.1)      # without this wait, the main thread exits too fast
                            # and we don't get to see the printouts from `on_close`
            break
