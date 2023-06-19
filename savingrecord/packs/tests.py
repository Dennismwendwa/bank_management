import unittest
from unittest.mock import patch
from io import StringIO
import random

from . quotes import money_quotes


class MoneyQuotesTest(unittest.TestCase):
    def test_money_quotes(self):
        quote = money_quotes()
        self.assertIsInstance(quote, str)
        self.assertTrue(quote.strip())  # Check that the quote is non-empty

if __name__ == '__main__':
    unittest.main()
