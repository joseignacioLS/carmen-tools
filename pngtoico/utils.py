import os
import re
import subprocess


def file_opener(func):
    def wrap(*args):
        try:
            with open(args[0]) as file:
                result = func(file)
            return result
        except FileNotFoundError:
            args[1].log(f"Archivo {args[0]} no encontrado", "ERR")
            quit()
    return wrap


def get_content_section(func):
    def wrap(*args):
        match = re.search(f"#{args[1]}[^#]+", args[0])
        if not match:
            return func([])
        return func(match.group().strip().split("\n")[1:])
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