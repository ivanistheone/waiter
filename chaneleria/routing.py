
from channels.routing import route
from chaneleria.consumers import ws_message

channel_routing = [
    route("websocket.receive", ws_message),
]