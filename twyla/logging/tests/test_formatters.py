import unittest
from logging import LogRecord, INFO, ERROR

from twyla.logging import formatters

class FormatterTests(unittest.TestCase):

    def test_extra_data_handler_plain(self):
        record = LogRecord('twyla.logging', INFO, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        formatter = formatters.ExtraDataFormatter(fmt='%(name)s - %(message)s - %(levelname)s')
        formatted = formatter.format(record)
        assert formatted == 'twyla.logging - The text message - INFO'



    def test_extra_data_handler_with_extra_data(self):
        record = LogRecord('twyla.logging', INFO, '/path/to/logging.py',
                           11, 'The text message', args=[],
                           exc_info=None, func='dostuff')
        record.lolwat = u'RÜFL'
        record.dadada = 'LALALA'
        formatter = formatters.ExtraDataFormatter(fmt='%(name)s - %(message)s - %(levelname)s')
        formatted = formatter.format(record)
        assert formatted == 'twyla.logging - The text message dadada: LALALA lolwat: RÜFL - INFO'
