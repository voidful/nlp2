import unittest

from nlp2.random import *


class TestRandom(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        print(random_string(10))


if __name__ == '__main__':
    unittest.main()
