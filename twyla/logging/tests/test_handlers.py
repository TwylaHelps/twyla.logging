import unittest
from unittest import mock
import json

from logging import LogRecord

from twyla.logging import handlers

class LogglyHTTPSHandlerTestCase(unittest.TestCase):

    def test_init(self):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        assert handler.url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'


    @mock.patch('twyla.logging.handlers.session')
    def test_handle_record(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        record = LogRecord('twyla.logging', 20, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        handler.emit(record)
        assert mock_session.post.call_count == 1
        _, (url,), kwargs = mock_session.post.mock_calls[0]
        assert url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'
        data = json.loads(kwargs['data'])
        assert data.pop('ascTime') == record.asctime
        assert data.pop('time') == record.msecs
        assert data.pop('logRecordCreationTime') == record.created
        assert data == {'loggerName': 'twyla.logging',
                        'fileName': 'logging.py',
                        'functionName': 'dostuff',
                        'levelNo': 20,
                        'lineNo': 11,
                        'levelName': 'INFO',
                        'message': 'The text message'}
