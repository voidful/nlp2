import unittest
from nlp2.file import *


class TestFile(unittest.TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
    DATA_DIR = os.path.join(ROOT_DIR, 'test/')

    def test_get_filename_from_path(self):
        paths = ['a/b/c/', 'a/b/c', '\\a\\b\\c', '\\a\\b\\c\\', 'a\\b\\c', 'a/b/../../a/b/c/', 'a/b/../../a/b/c']
        for path in paths:
            self.assertTrue('c' == get_filename_from_path(path))

    def test_get_folders_form_dir(self):
        for i in get_folders_from_dir(os.path.join(TestFile.DATA_DIR, './test_folder')):
            self.assertTrue(is_dir_exist(i))

    def test_get_files_from_dir(self):
        for i in get_files_from_dir(os.path.join(TestFile.DATA_DIR, './test_folder')):
            self.assertTrue(is_file_exist(i))

    def test_read_dir_files_yield_lines(self):
        self.assertCountEqual(list(read_dir_files_yield_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text/'))),
                              ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])
        self.assertCountEqual(list(read_dir_files_yield_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text'))),
                              ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])

    def test_read_dir_files_into_lines(self):
        self.assertCountEqual(read_dir_files_into_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text/')),
                              ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])
        self.assertCountEqual(read_dir_files_into_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text')),
                              ['abcabcabc', '天氣晴朗', '多雲', 'cbcbcb'])

    def test_read_files_yield_lines(self):
        self.assertEqual(list(read_files_yield_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text/file1'))),
                         ['abcabcabc', '天氣晴朗', '多雲'])

    def test_read_files_into_lines(self):
        self.assertEqual(read_files_into_lines(os.path.join(TestFile.DATA_DIR, './test_folder/text/file1')),
                         ['abcabcabc', '天氣晴朗', '多雲'])

    def test_create_new_dir_always(self):
        create_new_dir_always(os.path.join(TestFile.DATA_DIR, './test_folder/new'))
        self.assertTrue(is_dir_exist(os.path.join(TestFile.DATA_DIR, './test_folder/new')))

    def test_get_dir_with_notexist_create(self):
        get_dir_with_notexist_create(os.path.join(TestFile.DATA_DIR, './test_folder/new2'))
        self.assertTrue(is_dir_exist(os.path.join(TestFile.DATA_DIR, './test_folder/new2')))

    def test_is_file_exist(self):
        self.assertTrue(is_file_exist(os.path.join(TestFile.DATA_DIR, './test_folder/text/file1')))
        self.assertFalse(is_file_exist(os.path.join(TestFile.DATA_DIR, './test_folder/text/file100')))

    def test_is_dir_exist(self):
        self.assertTrue(is_dir_exist(os.path.join(TestFile.DATA_DIR, './test_folder/text')))
        self.assertFalse(is_dir_exist(os.path.join(TestFile.DATA_DIR, './test_folder/test')))

    def test_download_file(self):
        i = download_file(
            'https://raw.githubusercontent.com/voidful/voidful_blog/master/assets/post_src/nninmath_3/img1',
            os.path.join(TestFile.DATA_DIR, './test_folder/'))
        self.assertEqual(i, os.path.join(TestFile.DATA_DIR, './test_folder/img1'))

    def test_download_file_not_found(self):
        i = download_file(
            'https://dumps.wikimedia.org/abc/latest/', os.path.join(TestFile.DATA_DIR, './test_folder/'))
        self.assertEqual(i, "File not found")

    def test_write_csv(self):
        write_csv([["sent", "hi"]], os.path.join(TestFile.DATA_DIR, './test_folder/test.csv'))
        self.assertTrue(is_file_exist(os.path.join(TestFile.DATA_DIR, './test_folder/test.csv')))

    def test_csv_read(self):
        i = read_csv(os.path.join(TestFile.DATA_DIR, './test_folder/test.csv'))
        self.assertTrue(isinstance(list(i), list))

    def test_write_json(self):
        write_json({"sent": "hi"}, os.path.join(TestFile.DATA_DIR, './test_folder/test.json'))
        self.assertTrue(is_file_exist(os.path.join(TestFile.DATA_DIR, './test_folder/test.json')))

    def test_read_json(self):
        j = read_json(os.path.join(TestFile.DATA_DIR, './test_folder/test.json'))
        self.assertEqual(j, {"sent": "hi"})


if __name__ == '__main__':
    unittest.TestFile()
