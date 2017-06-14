"""
This module handles logs received via websockets.
"""
import json
import time

from .models import ContentChannelRun
from channels.sessions import channel_session
from django.http import Http404


@channel_session
def connect(message):
    # Expected path format: /logs/<run_id>/
    _, run_id = message['path'].strip('/').split('/')
    message.channel_session['run_id'] = run_id
    message.reply_channel.send({"accept": True})


@channel_session
def receive(message):
    """
    Stores logs in three files: all logs, error logs, critical logs.
    """
    run_id = message.channel_session['run_id']
    try:
        run = ContentChannelRun.objects.get(run_id=run_id)
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
