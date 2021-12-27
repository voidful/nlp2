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
    write_path = os.path.join(outdir, outfile)
    if not is_file_exist(write_path):
        try:
            urllib.request.urlretrieve(url, write_path, _progress)
        except Exception as e:
            print("Except:", e)
    print("\n")
    return write_path


def read_csv_row(fpath, chunksize=10000):
    from tqdm import tqdm
    import pandas as pd
    with open(fpath, encoding='utf8') as csvfile:
        it = pd.read_csv(csvfile, chunksize=chunksize, iterator=True)
        pbar = tqdm(it)
        try:
            for i, chunkdf in enumerate(pbar):
                for _, row in chunkdf.iterrows():
                    yield row
        finally:
            pbar.close()


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
