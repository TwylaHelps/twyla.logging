import logging
import logging.handlers
import json

import socket
import traceback

from requests_futures.sessions import FuturesSession

session = FuturesSession()

URL_BASE =  'https://logs-01.loggly.com/inputs/{token}/tag/{tag}'

def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass


class LogglyHTTPSHandler(logging.Handler):
    def __init__(self, token, tag):
        logging.Handler.__init__(self)
        self.url = URL_BASE.format(**locals())

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        return record.getMessage()

    def emit(self, record):
        data = {
            'loggerName': record.name,
            'ascTime': record.asctime,
            'fileName': record.filename,
            'logRecordCreationTime': record.created,
            'functionName': record.funcName,
            'levelNo': record.levelno,
            'lineNo': record.lineno,
            'time': record.msecs,
            'levelName': record.levelname,
            'message': record.message
        }
        try:
            payload = json.dumps(data)
            session.post(self.url, data=payload, background_callback=bg_cb)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
