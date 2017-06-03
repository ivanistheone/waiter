#!/usr/bin/env python

import logging
import time


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


if __name__ == '__main__':
    progress = ProgressConsoleHandler()

    logger = logging.getLogger('sushi-chef-name')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(progress)


    logger.info('Testing some info message')

    for i in range(3):
        logger.info('remaining %d seconds', i, extra={'same_line':True})
        time.sleep(1)

    logger.info('another info msg yo')

