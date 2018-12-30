import unittest

from nlp2.text import *


class TestText(unittest.TestCase):

    def text_remove_httplink(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_lines_in_sentence(self):
        print(passage_into_chunk("xxxxxxxx\noo\nyyzz\ngggggg\nkkkk\n",10))
        # print(text_into_chunk_by_lines(['你好', 'are', "可以"]))\
        print(full2half("，,"))
        print(half2full("，,"))


    def test_remove_httplink(self):
        result = remove_httplink("http://news.IN1802020028.htm 今天天氣http://news.we028.晴朗")
        print(result)



if __name__ == '__main__':
    unittest.main()
