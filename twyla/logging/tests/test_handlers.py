import sys
import unittest
from unittest import mock
import json

from logging import LogRecord, INFO, ERROR

from twyla.logging import handlers

class LogglyHTTPSHandlerTestCase(unittest.TestCase):

    def test_init(self):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        assert handler.url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'


    @mock.patch('twyla.logging.handlers.session')
    def test_handle_record(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        record = LogRecord('twyla.logging', INFO, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        handler.emit(record)
        assert mock_session.post.call_count == 1
        _, (url,), kwargs = mock_session.post.mock_calls[0]
        assert url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'
        data = json.loads(kwargs['data'])
        assert data.pop('timestamp') == record.asctime
        assert data.pop('time') == record.msecs
        assert data.pop('logRecordCreationTime') == record.created
        assert data == {'loggerName': 'twyla.logging',
                        'fileName': 'logging.py',
                        'functionName': 'dostuff',
                        'levelNo': INFO,
                        'lineNo': 11,
                        'levelName': 'INFO',
                        'message': 'The text message'}


    @mock.patch('twyla.logging.handlers.session')
    def test_extra_attributes(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        record = LogRecord('twyla.logging', INFO, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        record.an_attribute = 555
        record.other_attribute = 'Hello there'
        handler.emit(record)
        assert mock_session.post.call_count == 1
        _, _, kwargs = mock_session.post.mock_calls[0]
        data = json.loads(kwargs['data'])
        assert data.pop('extra') == {'an_attribute': 555,
                                     'other_attribute': 'Hello there'}
        assert data.pop('timestamp') == record.asctime
        assert data.pop('time') == record.msecs
        assert data.pop('logRecordCreationTime') == record.created
        assert data == {'loggerName': 'twyla.logging',
                        'fileName': 'logging.py',
                        'functionName': 'dostuff',
                        'levelNo': INFO,
                        'lineNo': 11,
                        'levelName': 'INFO',
                        'message': 'The text message'}


    @mock.patch('twyla.logging.handlers.session')
    def test_stacktrace(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        try:
            raise ValueError()
        except:
            exc_info = sys.exc_info()
        record = LogRecord('twyla.logging', ERROR, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=exc_info, func='dostuff')
        handler.emit(record)
        assert mock_session.post.call_count == 1
        _, _, kwargs = mock_session.post.mock_calls[0]
        data = json.loads(kwargs['data'])
        assert data.pop('timestamp') == record.asctime
        assert data.pop('time') == record.msecs
        assert data.pop('logRecordCreationTime') == record.created
        message_lines = data.pop('message').split('\n')
        assert message_lines[0] == 'The text message'
        assert message_lines[1] == 'Traceback (most recent call last):'
        assert data == {'loggerName': 'twyla.logging',
                        'fileName': 'logging.py',
                        'functionName': 'dostuff',
                        'levelNo': ERROR,
                        'lineNo': 11,
                        'levelName': 'ERROR'}


    @mock.patch('twyla.logging.handlers.session')
    def test_binary_data(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        record = LogRecord('twyla.logging', ERROR, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        record.binary_attribute = b'Binary string'
        handler.emit(record)
        assert mock_session.post.call_count == 1
        _, _, kwargs = mock_session.post.mock_calls[0]
