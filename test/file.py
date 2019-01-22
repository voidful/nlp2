import unittest
from nlp2.file import *


class TestFile(unittest.TestCase):

    def test_get_folders_form_dir(self):
        for i in get_folders_form_dir('./test_floder'):
            self.assertTrue(is_dir_exist(i))

    def test_get_files_from_dir(self):
        for i in get_files_from_dir('./test_floder'):
            self.assertTrue(is_file_exist(i))

    def test_read_dir_files_yield_lines(self):
        self.assertEqual(list(read_dir_files_yield_lines('./test_floder/text/')), ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])
        self.assertEqual(list(read_dir_files_yield_lines('./test_floder/text')), ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])

    def test_read_dir_files_into_lines(self):
        self.assertEqual(read_dir_files_into_lines('./test_floder/text/'), ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])
        self.assertEqual(read_dir_files_into_lines('./test_floder/text'), ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])

    def test_read_files_yield_lines(self):
        self.assertEqual(list(read_files_yield_lines('./test_floder/text/file1')), ['abcabcabc', '天氣晴朗', '多雲'])

    def test_read_files_into_lines(self):
        self.assertEqual(read_files_into_lines('./test_floder/text/file1'), ['abcabcabc', '天氣晴朗', '多雲'])

    def test_create_new_dir_always(self):
        create_new_dir_always('./test_floder/new')
        self.assertTrue(is_dir_exist('./test_floder/new'))

    def test_get_dir_with_notexist_create(self):
        get_dir_with_notexist_create('./test_floder/new2')
        self.assertTrue(is_dir_exist('./test_floder/new2'))

    def test_write_json_to_file(self):
        write_json_to_file({"sent": "hi"}, './test_floder/test.json')
        self.assertTrue(is_file_exist('./test_floder/test.json'))

    def test_is_file_exist(self):
        self.assertTrue(is_file_exist('./test_floder/text/file1'))
        self.assertFalse(is_file_exist('./test_floder/text/file100'))

    def test_is_dir_exist(self):
        self.assertTrue(is_dir_exist('./test_floder/text'))
        self.assertFalse(is_dir_exist('./test_floder/test'))

    def test_download_file(self):
        i = download_file(
            'https://raw.githubusercontent.com/voidful/voidful_blog/master/assets/post_src/nninmath_3/img1',
            './test_floder/')
        self.assertEqual(i, './test_floder/img1')

    def test_download_file_not_found(self):
        i = download_file(
            'https://dumps.wikimedia.org/abc/latest/', './test_floder/')
        self.assertEqual(i, "File not found")


if __name__ == '__main__':
    unittest.TestFile()
