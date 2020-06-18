import unittest

from nlp2.rand import *


class TestRandom(unittest.TestCase):

    def test_random_string(self):
        self.assertEqual(len(random_string(3)), 3)
        self.addTypeEqualityFunc(str, random_string(3))

    def test_random_string_with_timestamp(self):
        self.assertEqual(len(random_string_with_timestamp(3)), 10 + 3)
        self.addTypeEqualityFunc(str, random_string_with_timestamp(3))

    def test_random_value_in_array_form(self):
        self.assertEqual(random_value_in_array_form([3, 3]), 3)
        self.assertEqual(random_value_in_array_form([3.0, 3.0]), 3)
        self.assertEqual(random_value_in_array_form(['A', 'A']), 'A')


if __name__ == '__main__':
    unittest.main()
