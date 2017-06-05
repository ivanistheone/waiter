
# from django.http import HttpResponse
# from channels.handler import AsgiHandler
import logging
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)


def ws_message(message):
    """
    Fallback consumer for all WebSocket messages.
    """
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    pp.pprint(message.__dict__)
    # data_from_text = json.loads(message.content['text'])
    # print(data_from_text.keys())
    message.reply_channel.send({
        "text": 'python socket replies with:' + message.content['text'],
    })


def log_message(message):
    """
    WebSocket endpoint for receiving sushi chef log streaming messages.
    """
    print('In log_message websocket receive handler')
    message_data = json.loads(message.content['text'])
    pp.pprint(message_data)
    log_id = message_data['log_id']

    # Recreate the LogRecord object and produce a formatted logline string
    log_record_data = dict(
        name=message_data['name'],
        level=message_data['levelno'],
        pathname=message_data['pathname'],
        lineno=message_data['lineno'],
        msg=message_data['msg'],
        args=tuple(message_data['args']),
        exc_info=message_data['exc_info'],
        func=message_data['funcName'],
    )
    log_record = logging.LogRecord(**log_record_data)
    detaild_fmt = '%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s\n'
    formatter = logging.Formatter(detaild_fmt)
    logline_str = formatter.format(log_record)
    # print(logline_str)

    # Append logline to appropriate file log storage directory
    log_filename = os.path.join('/tmp', 'sushicheflogs', str(log_id)+'.log')
    with open(log_filename, 'a') as logfile:
        logfile.write(logline_str)

    # Respond with OK
    message.reply_channel.send({
        "text": 'acknolwedge log received',
    })
