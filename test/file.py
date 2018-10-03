import unittest
from nlp2 import file

class TestFile(unittest.TestCase):

    def get_folders_form_dir(self):
        file.get_folders_form_dir('')

    def get_files_from_dir(self, match=""):
        for path, subdirs, files in os.walk(self):
            for file in files:
                if len(match) > 0:
                    if file in match:
                        yield path + file
                else:
                    yield os.path.join(path, file)

    def read_dir_files_into_lines(dir_path):
        for file in os.listdir(dir_path):
            with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
                for line in f:
                    yield line

    def read_files_into_lines(path):
        with open(path, "r", encoding='utf-8') as file:
            for line in file:
                yield line

    def create_new_dir(dirPath):
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        else:
            file_list = os.listdir(dirPath)
            for fileName in file_list:
                os.remove(dirPath + "/" + fileName)


if __name__ == '__main__':
    unittest.main()
