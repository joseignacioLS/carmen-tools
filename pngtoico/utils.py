import os


def load_file(path, callback, error_callback):
    try:
        with open(path) as file:
            return callback(file)
    except FileNotFoundError:
        error_callback(path)


def create_folder(path, callback, error_callback):
    try:
        os.mkdir(path)
        callback(path)
    except FileExistsError:
        error_callback(path)
