from channels.routing import route
from runs import ws_logs

channel_routing = [
    route("websocket.connect", ws_logs.connect, path=r"^/logs/"),
    route("websocket.receive", ws_logs.receive, path=r"^/logs/"),
]
