import os
from PIL import Image
import subprocess
import re
from logger import Logger
from utils import load_file, create_folder
from contants import LOG_FILE, DATA_FILE


def get_resolutions(file_content):
    res_match = re.search("#Resoluciones[^#]+", file_content)
    if not res_match:
        logger.log("No existen resoluciones", "ERR")
        quit()
    return [(int(x), int(x)) for x in res_match.group().strip().split("\n")[1:]]


def get_names(file_content):
    icon_names = {}
    name_match = re.search("#Nombres[^#]+", file_content)
    if name_match:
        for pair in name_match.group().strip().split("\n")[1:]:
            original, mod = pair.strip().split("\t")
            icon_names[original] = mod
    return icon_names


def process_data_content(file):
    content = file.read()
    icon_sizes = get_resolutions(content)
    icon_names = get_names(content)
    return icon_sizes, icon_names


def load_data_file():
    def on_error(path):
        logger.log(f"No se encuentra el archivo {path}", "ERR")
        quit()
    data = load_file(
        DATA_FILE,
        process_data_content,
        on_error
    )
    return data


def get_icon_name(icon_name, icon_names):
    if icon_name in icon_names:
        return icon_names[icon_name]
    return icon_name


def process_file(path, icon_sizes, icon_names):
    img = Image.open(path)
    name = get_icon_name(path[:-4], icon_names)
    img.save(name + ".ico", sizes=icon_sizes, bitmap_format="bmp")
    logger.log(f"Archivo {path} salvado como {name}.ico", "MSG")
    subprocess.call(f"copy {path} png\\{path} /y", shell=True)
    subprocess.call(f"del {path}", shell=True)


def main():
    create_folder(
        "png",
        lambda path: logger.log(f"Carpeta {path} creada", "MSG"),
        lambda path: logger.log(f"Carpeta {path} ya existe", "MSG")
    )

    icon_sizes, icon_names = load_data_file()

    file_list = [x for x in os.listdir() if ".png" in x]
    if len(file_list) == 0:
        logger.log("No hay archivos png", "WAR")

    for archivo in file_list:
        process_file(archivo, icon_sizes, icon_names)


if __name__ == "__main__":
    logger = Logger(LOG_FILE)
    logger.log("Starting", "MSG")
    main()
    logger.log("End", "MSG")
