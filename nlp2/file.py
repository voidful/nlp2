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


def read_dir_files_into_lines(dir_path):
    for file in os.listdir(dir_path):
        with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
            for line in f:
                yield line


def read_files_into_lines(path):
    with open(path, "r", encoding='utf-8') as file:
        for line in file:
            yield line
