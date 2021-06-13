import json
import os
import re
import sys
import urllib.request
import csv


def get_folders_from_dir(root, match=""):
    for path, subdirs, files in os.walk(root):
        if path != root:
            yield path


def get_filename_from_path(path):
    """Extracts basename of a given path. Should Work with any OS Path on any OS"""
    basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
    if basename:
        return basename.group(0)


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
                yield line.strip()


def read_dir_files_into_lines(dir_path):
    ret = []
    for file in os.listdir(dir_path):
        with open(os.path.join(dir_path, file), "r", encoding="utf8") as f:
            ret += f.read().splitlines()
    return ret


def read_files_yield_lines(path):
    with open(path, "r", encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def read_files_into_lines(path):
    with open(path, "r", encoding='utf-8') as file:
        return file.read().splitlines()


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


def is_file_exist(file_loc):
    return os.path.isfile(file_loc)


def is_dir_exist(file_dir):
    return os.path.isdir(file_dir)


def _progress(block_num, block_size, total_size):
    sys.stdout.write('\r>> Downloading %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


def download_file(url, outdir):
    outdir = get_dir_with_notexist_create(outdir)
    outfile = url.split('/')[-1]
    if not is_file_exist(outdir + outfile):
        try:
            urllib.request.urlretrieve(url, outdir + outfile, _progress)
        except:
            return "File not found"
    sys.stdout.write("\n")
    return outdir + outfile


def read_csv(filepath, delimiter=None):
    sniffer = csv.Sniffer()
    with open(filepath, encoding='utf8') as f:
        line = f.readline()
        if delimiter is None:
            dialect = sniffer.sniff(line)
            delimiter = dialect.delimiter
        f.seek(0)
        cf = csv.reader(f, delimiter=delimiter)
        return list(cf)


def write_csv(csv_rows, loc):
    with open(loc, 'w', encoding='utf8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(csv_rows)


def read_json(filepath):
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
        return data


def write_json(json_str, loc):
    with open(loc, 'w', encoding='utf-8') as outfile:
        json.dump(json_str, outfile, indent=4, ensure_ascii=False)
    return loc
