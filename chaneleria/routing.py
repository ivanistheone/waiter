
from channels.routing import route
from chaneleria.consumers import ws_message, log_message

# http_routing = [
#     route("http.request", sushibar_api, path=r"^/api/$"),     # TODO
# ]

channel_routing = [
    route("websocket.receive", log_message, path=r"^/logs/$"),
    route("websocket.receive", ws_message),
    # include(http_routing),
]
