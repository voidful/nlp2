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


def rm_path_content(path):
    import shutil
    try:
        shutil.rmtree(path)
        return True
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")
        return False


def get_file_from_dir_by_create_time(dir, match=""):
    return [str(i) for i in sorted(Path(dir).iterdir(), key=creation_date, reverse=True) if match in str(i)]


def get_files_from_dir(root, match="", creation_date_after='', creation_date_x_days_ago=0):
    for path, subdirs, files in os.walk(root):
        for file in sorted(files, reverse=True):
            filepath = os.path.join(path, file)
            if not is_file_exist(filepath):
                continue
            if len(match) > 0 and match not in file:
                continue
            if len(creation_date_after) > 0 or creation_date_x_days_ago > 0:
                create_date = datetime.fromtimestamp(os.path.getatime(filepath))
                if creation_date_x_days_ago > 0:
                    in_range_date = datetime.fromordinal(datetime.today().toordinal() - creation_date_x_days_ago)
                else:
                    in_range_date = datetime.fromisoformat(creation_date_after)
                if in_range_date > create_date:
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
    progress = (block_num * block_size) / total_size * 100.0
    sys.stdout.write(f'\r>> Downloading {progress:.1f}%')
    sys.stdout.flush()


def recu_down(url, filename, show_progress):
    """Recurrent download with handling for ContentTooShortError."""
    try:
        if show_progress:
            urllib.request.urlretrieve(url, filename, _progress)
        else:
            urllib.request.urlretrieve(url, filename)
    except urllib.error.ContentTooShortError:
        print('Network conditions are not good. Reloading...')
        recu_down(url, filename, show_progress)


def download_file(url, outdir, new_filename=None, show_progress=False):
    """
    Downloads a file from a URL, retrying on network issues.

    Parameters:
        url (str): The URL of the file to download.
        outdir (str): The directory where the file will be saved.
        new_filename (str, optional): The new name for the downloaded file. If None, the original name from the URL is used.
        show_progress (bool, optional): Whether to show the progress bar. Defaults to False.

    Returns:
        str: The path to the downloaded file.
    """
    outdir = get_dir_with_notexist_create(outdir)
    outfile = new_filename if new_filename else url.split('/')[-1]
    write_path = os.path.join(outdir, outfile)

    if not is_file_exist(write_path):
        recu_down(url, write_path, show_progress)

    if show_progress:
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


class JSONEncoderWithNumpy(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def write_json(json_str, loc):
    with open(loc, 'w', encoding='utf-8') as outfile:
        json.dump(json_str, outfile, indent=4, sort_keys=False, ensure_ascii=False, cls=JSONEncoderWithNumpy)
    return loc


def write_jsonl(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item, sort_keys=False, ensure_ascii=False) + "\n")


def read_jsonl(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield json.loads(line)
