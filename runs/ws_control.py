"""
This module receives control commands and forwards them to sushi chefs.
"""
import json
import time

from .models import ContentChannelRun
from channels.sessions import channel_session
from channels import Group
from django.http import Http404


@channel_session
def connect(message):
    # Expected path format: /control/<channel_id>/
    _, channel_id = message['path'].strip('/').split('/')
    Group('control-' + channel_id).add(message.reply_channel)
    message.channel_session['channel_id'] = channel_id
    message.reply_channel.send({"accept": True})


@channel_session
def receive(message):
    """
    Stores logs in three files: all logs, error logs, critical logs.
    """
    channel_id = message.channel_session['channel_id']
    try:
        run = ContentChannelRun.objects.get(channel_id=channel_id)
        logfile = run.logfile.path
    except ContentChannelRun.DoesNotExist:
        raise Http404
    record = json.loads(message['text'])
    timestamp = time.localtime(float(record['created']))
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
    log = '%s - %s - %s - %s - %d - %s' % (
        record['levelname'], timestamp, record['filename'],
        record['funcName'], record['lineno'], record['message'])
    with open(logfile, 'a') as f:
        f.write(log + '\n')
    if record['levelname'] == 'ERROR':
        with open(logfile+'.error', 'a') as f:
            f.write(log + '\n')
    if record['levelname'] == 'CRITICAL':
        with open(logfile + '.critical', 'a') as f:
            f.write(log + '\n')


@channel_session
def disconnect(message):
    pass
