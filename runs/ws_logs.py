import json

from channels.sessions import channel_session


@channel_session
def connect(message):
    _, run_id = message['path'].strip('/').split('/')
    message.channel_session['run_id'] = run_id
    message.reply_channel.send({"accept": True})


@channel_session
def receive(message):
    run_id = message.channel_session['run_id']
    record = json.loads(message['text'])
    log = '%s - %s - %s - %s - %d - %s' % (
        record['levelname'], record['created'], record['filename'],
        record['funcName'], record['lineno'], record['message'])
    print(">>>M %s, %s" % (run_id, log))


@channel_session
def disconnect(message):
    run_id = message.channel_session['run_id']
    print(">>> Disconnect: %s" % run_id)
