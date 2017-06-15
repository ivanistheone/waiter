"""
This module receives control commands and forwards them to sushi chefs.
"""
from channels.sessions import channel_session
from channels import Group


@channel_session
def connect(message):
    # Expected path format: /control/<channel_id>/
    _, channel_id = message['path'].strip('/').split('/')
    print("Control connecting %s" % channel_id)
    Group('control-' + channel_id).add(message.reply_channel)
    message.channel_session['channel_id'] = channel_id
    message.reply_channel.send({"accept": True})


@channel_session
def receive(message):
    channel_id = message.channel_session['channel_id']
    print("Receive control %s, %s" % (channel_id, message['text']))
    Group('control-'+channel_id).send({'text': message['text']})


@channel_session
def disconnect(message):
    channel_id = message.channel_session['channel_id']
    print("Control disconnecting %s" % channel_id)
