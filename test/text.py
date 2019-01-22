import unittest
from nlp2.text import *


class TestText(unittest.TestCase):

    def test_remove_httplink(self):
        self.assertEqual(remove_httplink("http://news.IN1802020028.htm 今天天氣http://news.we028.晴朗"), "今天天氣 晴朗")

    def test_split_lines_by_punc(self):
        self.assertEqual(split_lines_by_punc(["你好啊.hello，me"]), ['你好啊', 'hello', 'me'])

    def test_split_sentence_to_ngram(self):
        self.assertEqual(split_sentence_to_ngram("加州旅館"), ['加', '加州', "加州旅", "加州旅館", "州", "州旅", "州旅館", "旅", "旅館", "館"])

    def test_split_sentence_to_ngram_in_part(self):
        self.assertEqual(split_sentence_to_ngram_in_part("加州旅館"),
                         [['加', '加州', "加州旅", "加州旅館"], ["州", "州旅", "州旅館"], ["旅", "旅館"], ["館"]])

    def test_spilt_text_in_all_ways(self):
        self.assertEqual(spilt_text_in_all_ways("加州旅館"),
                         ['加 州 旅 館', '加 州 旅館', '加 州旅 館', '加 州旅館', '加州 旅館', '加州旅 館', '加州旅館'])

    def test_spilt_sentence_to_array(self):
        self.assertEqual(spilt_sentence_to_array('你好 are  u 可以'), ['你好', 'are', 'u', '可以'])
        self.assertEqual(spilt_sentence_to_array('你好 are  u 可以', True), ['你', '好', 'are', 'u', '可', '以'])

    def test_join_words_array_to_sentence(self):
        self.assertEqual(join_words_array_to_sentence(['你好', 'are', "可以"]), "你好are可以")

    def test_passage_into_chunk(self):
        self.assertEqual(passage_into_chunk("xxxxxxxx\noo\nyyzz\ngggggg\nkkkk\n", 10),
                         ['xxxxxxxx oo ', 'yyzz gggggg ', 'kkkk '])

    def test_is_all_english(self):
        self.assertTrue(is_all_english("1SGD"))
        self.assertFalse(is_all_english("1SG哦"))

    def test_is_contain_number(self):
        self.assertTrue(is_contain_number("1SGD"))
        self.assertFalse(is_contain_number("SG哦"))

    def test_is_contain_english(self):
        self.assertTrue(is_contain_english("1SGD"))
        self.assertFalse(is_contain_english("1哦"))

    def test_full2half(self):
        self.assertEqual(full2half("，,"), ",,")

    def test_half2full(self):
        self.assertEqual(half2full("，,"), "，，")


if __name__ == '__main__':
    unittest.main()
