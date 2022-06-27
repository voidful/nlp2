import csv
import json
import os
import platform
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def get_folders_from_dir(root, match=""):
    for path, subdirs, files in os.walk(root):
        if path != root:
            yield path


def get_filename_from_path(path):
    """Extracts basename of a given path. Should Work with any OS Path on any OS"""
    basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
    if basename:
        return basename.group(0)


def get_file_from_dir_by_create_time(dir, match=""):
    return [str(i) for i in sorted(Path(dir).iterdir(), key=creation_date, reverse=True) if match in str(i)]


def get_files_from_dir(root, match="", creation_date_after='', creation_date_x_days_ago=0):
    for path, subdirs, files in os.walk(root):
        for file in files:
            if len(creation_date_after) > 0 or creation_date_x_days_ago > 0:
                create_date = datetime.fromtimestamp(creation_date(os.path.join(path, file)))
                if creation_date_x_days_ago > 0:
                    after_date = datetime.fromordinal(datetime.today().toordinal() - creation_date_x_days_ago)
                else:
                    after_date = datetime.fromisoformat(creation_date_after)
                if not create_date > after_date:
                    continue
            if len(match) > 0:
                if match not in file:
                    continue
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
    write_path = os.path.join(outdir, outfile)
    if not is_file_exist(write_path):
        try:
            urllib.request.urlretrieve(url, write_path, _progress)
        except Exception as e:
            print("Except:", e)
    print("\n")
    return write_path


def read_csv(filepath, delimiter=','):
    sniffer = csv.Sniffer()
    with open(filepath, encoding='utf8') as f:
        line = f.readline()
        if delimiter is None:
            dialect = sniffer.sniff(line)
            delimiter = dialect.delimiter
        f.seek(0)
        cf = csv.reader(f, delimiter=delimiter)
        return list(cf)


def read_csv_chunk(filepath, delimiter=',', chunksize=70000):
    sniffer = csv.Sniffer()
    with open(filepath, encoding='utf8') as f:
        line = f.readline()
        if delimiter is None:
            dialect = sniffer.sniff(line)
            delimiter = dialect.delimiter
        f.seek(0)
        cf = csv.reader(f, delimiter=delimiter)
        chunk = []
        for i, line in enumerate(cf):
            if (i % chunksize == 0 and i > 0):
                yield chunk
                del chunk[:]  # or: chunk = []
            chunk.append(line)
        yield chunk


def write_csv(csv_rows, loc, delimiter=None):
    with open(loc, 'w', encoding='utf8') as outfile:
        if delimiter is not None:
            writer = csv.writer(outfile, delimiter=delimiter)
        else:
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
