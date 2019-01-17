import unittest
from nlp2 import file
import os


class TestFile(unittest.TestCase):

    def test_download_file(self):
        i = file.download_file(
            'https://raw.githubusercontent.com/voidful/voidful_blog/master/assets/post_src/nninmath_3/img1', './')
        self.assertEqual(i, './img1')
        print(i)

    def test_download_file_not_found(self):
        i = file.download_file(
            'https://dumps.wikimedia.org/abc/latest/', './')
        self.assertEqual(i, "File not found")
        print(i)

    # def get_folders_form_dir(self):
    #     file.get_folders_form_dir('')
    #
    # def get_files_from_dir(self, match=""):
    #     for path, subdirs, files in os.walk(self):
    #         for file in files:
    #             if len(match) > 0:
    #                 if file in match:
    #                     yield path + file
    #             else:
    #                 yield os.path.join(path, file)
    #
    # def read_dir_files_into_lines(self, dir_path):
    #     for file in os.listdir(dir_path):
    #         with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
    #             for line in f:
    #                 yield line
    #
    # def read_files_into_lines(self, path):
    #     with open(path, "r", encoding='utf-8') as file:
    #         for line in file:
    #             yield line
    #
    # def create_new_dir(self, dirPath):
    #     if not os.path.exists(dirPath):
    #         os.makedirs(dirPath)
    #     else:
    #         file_list = os.listdir(dirPath)
    #         for fileName in file_list:
    #             os.remove(dirPath + "/" + fileName)


if __name__ == '__main__':
    unittest.TestFile()
