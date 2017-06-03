#!/usr/bin/env python3
# pip3 install websocket-client

import websocket
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8000/chat")

ws.send('client says hello')

print( ws.recv() )
print( ws.recv() )

