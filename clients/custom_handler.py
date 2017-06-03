#!/usr/bin/env python
import datetime
import json
import logging
import time


# via https://stackoverflow.com/questions/3118059/how-to-write-custom-python-logging-handler
class ProgressConsoleHandler(logging.StreamHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """
    on_same_line = False
    def emit(self, record):
        # print(record.__dict__)
        try:
            msg = self.format(record)
            stream = self.stream
            same_line = hasattr(record, 'same_line')
            if self.on_same_line and not same_line:
                stream.write(self.terminator)
            stream.write(msg)
            if same_line:
                stream.write('... ')
                self.on_same_line = True
            else:
                stream.write(self.terminator)
                self.on_same_line = False
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# via http://masnun.com/2015/11/04/python-writing-custom-log-handler-and-formatter.html
class CustomFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name
        super(CustomFormatter, self).__init__()
 
    def format(self, record):
        data = {'@message': record.msg % record.args,
                '@timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                '@type': 'ricecooker-log-entry'}
 
        if self.task_name:
            data['@task_name'] = self.task_name
 
        return json.dumps(data)


if __name__ == '__main__':
    logger = logging.getLogger('sushi-chef-name')
    logger.setLevel(logging.DEBUG)

    progress_handler = ProgressConsoleHandler()
    formatter = CustomFormatter(task_name='some task name')
    progress_handler.setFormatter(formatter)

    logger.addHandler(progress_handler)

    logger.info('Testing some info message')

    for i in range(3):
        logger.info('remaining %d seconds', i, extra={'same_line':True})
        time.sleep(1)

    logger.info('another info msg yo')

