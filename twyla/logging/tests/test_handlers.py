import unittest
from unittest import mock
from logging import LogRecord

from twyla.logging import handlers

class LogglyHTTPSHandlerTestCase(unittest.TestCase):

    def test_init(self):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        assert handler.url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'


    @mock.patch('twyla.logging.handlers.session')
    def test_handle_record(self, mock_session):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        record = LogRecord('name', 'level', 'pathname', 'lineno', 'msg', [], None)
        handler.emit(record)
        assert mock_session.post.call_count == 1
