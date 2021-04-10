import unittest
from nlp2.panel import *


class TestPanel(unittest.TestCase):

    def test_Empty(self):
        def a():
            pass

        argument = function_argument_panel(a)
        self.assertEqual(len(argument), 0)

    def test_None(self):
        def a(a):
            pass

        argument = function_argument_panel(a)
        self.assertEqual(len(argument), 0)

    def test_Pred(self):
        def a(input):
            pass

        argument = function_argument_panel(a)
        self.assertEqual(len(argument), 0)

    def test_Pred(self):
        def a(input=''):
            pass

        argument = function_argument_panel(a, disable_input_panel=True)
        self.assertEqual(argument['input'], '')

        argument = function_argument_panel(a, ignore_empty=True)
        self.assertEqual(argument['input'], '')

    def test_function_sep_suit_arg(self):
        def a(c="a"):
            pass

        suit_argument, others_argument = function_sep_suit_arg(a, {"c": "a", "b": "d"})
        self.assertEqual(suit_argument, {'c': "a"})
        self.assertEqual(others_argument, {'b': "d"})

    def test_Default(self):
        def a(c="a"):
            pass

        argument = function_argument_panel(a, disable_input_panel=True)
        self.assertEqual(argument['c'], 'a')

    def test_missing(self):
        def a(c="a"):
            pass

        missing = function_check_missing_arg(a, {'d': "a"})
        self.assertEqual(missing, ['c'])
        wrong = function_check_wrong_arg(a, {'d': "a"})
        self.assertEqual(wrong, ['d'])

        missing = function_check_missing_arg(a, {'c': "a"})
        self.assertEqual(missing, [])
        wrong = function_check_wrong_arg(a, {'c': "a"})
        self.assertEqual(wrong, [])

        class B():
            def a(self, c="a"):
                pass

        b = B()
        missing = function_check_missing_arg(b.a, {'c': "a"})
        self.assertEqual(missing, [])
        wrong = function_check_wrong_arg(b.a, {'c': "a"})
        self.assertEqual(wrong, [])

    if __name__ == '__main__':
        unittest.main()
