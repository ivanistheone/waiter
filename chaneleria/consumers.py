
# from django.http import HttpResponse
# from channels.handler import AsgiHandler
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)



def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    pp.pprint(message.__dict__)
    data_from_text = json.loads(message.content['text'])
    print(data_from_text.keys())
    message.reply_channel.send({
        "text": 'python socket replies with:' + message.content['text'],
    })
    
