
# from django.http import HttpResponse
# from channels.handler import AsgiHandler

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    # print(message.__dict__)
    message.reply_channel.send({
        "text": 'python socket replies with:' + message.content['text'],
    })
    
