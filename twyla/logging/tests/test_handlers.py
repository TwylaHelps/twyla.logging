import unittest

from twyla.logging import handlers

class LogglyHTTPSHandlerTestCase(unittest.TestCase):

    def test_init(self):
        handler = handlers.LogglyHTTPSHandler('abcd-123', 'python')
        assert handler.url == 'https://logs-01.loggly.com/inputs/abcd-123/tag/python'
