from channels.routing import route
from runs import ws_logs
from runs import ws_control

channel_routing = [
    route("websocket.connect", ws_logs.connect, path=r"^/logs/"),
    route("websocket.receive", ws_logs.receive, path=r"^/logs/"),
    route("websocket.connect", ws_control.connect, path=r"^/control/"),
    route("websocket.receive", ws_control.receive, path=r"^/control/"),
    route("websocket.disconnect", ws_control.disconnect, path=r"^/control/"),
]
