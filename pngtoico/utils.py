import os
import re
import subprocess
import sys


def file_opener(func):
    def wrap(*args, **kwargs):
        try:
            with open(kwargs["data_file"]) as file:
                result = func(*args, file)
            return result
        except FileNotFoundError:
            kwargs["logger"].log(f"Archivo {kwargs['data_file']} no encontrado", "ERR")
            sys.exit()
    return wrap


def get_content_section(func):
    def get_content_lines(content):
        return content.strip().split("\n")[1:]

    def wrap(*args, **kwargs):
        match = re.search(f"#{kwargs['section']}[^#]+", kwargs['content'])
        return func(*args, get_content_lines(match.group()) if match else [])

    return wrap


def create_folder(path, callback, error_callback):
    try:
        os.mkdir(path)
        callback(path)
    except FileExistsError:
        error_callback(path)


def move_file(origin_path, destination_path):
    subprocess.call(f"copy {origin_path} {destination_path} /y", shell=True)
    subprocess.call(f"del {origin_path}", shell=True)
