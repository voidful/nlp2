import json
import os


def get_folders_form_dir(root, match=""):
    for path, subdirs, files in os.walk(root):
        if path != root:
            yield path


def get_files_from_dir(root, match=""):
    for path, subdirs, files in os.walk(root):
        for file in files:
            if len(match) > 0:
                if file in match:
                    yield path + file
            else:
                yield os.path.join(path, file)


def read_dir_files_yield_lines(dir_path):
    for file in os.listdir(dir_path):
        with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
            for line in f:
                yield line


def read_dir_files_into_lines(dir_path):
    ret = []
    for file in os.listdir(dir_path):
        with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
            ret += f.readlines()
    return ret


def read_files_yield_lines(path):
    with open(path, "r", encoding='utf-8') as file:
        for line in file:
            yield line


def read_files_into_lines(path):
    with open(path, "r", encoding='utf-8') as file:
        return file.readlines()


def create_new_dir_always(dirPath):
    if not is_dir_exist(dirPath):
        os.makedirs(dirPath)
    else:
        file_list = os.listdir(dirPath)
        for fileName in file_list:
            os.remove(dirPath + "/" + fileName)


def get_dir_with_notexist_create(dirPath):
    if not is_dir_exist(dirPath):
        os.makedirs(dirPath)
    return dirPath


def write_json_to_file(json_str, loc):
    with open(loc, 'w', encoding='utf-8') as outfile:
        json.dump(json_str, outfile, indent=4, ensure_ascii=False)
    return loc


def is_file_exist(file_loc):
    return os.path.isfile(file_loc)


def is_dir_exist(file_dir):
    return os.path.isdir(file_dir)
