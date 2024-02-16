import os
from PIL import Image
from logger import Logger
from utils import file_opener, create_folder, get_content_section, move_file
from contants import LOG_FILE, DATA_FILE


@get_content_section
def get_resolutions(data):
    resolutions = [(int(x), int(x)) for x in data]
    if len(resolutions) == 0:
        logger.log("No existen resoluciones", "ERR")
        quit()
    return resolutions


@get_content_section
def get_names(data):
    names = {x.strip().split("\t")[0]: x.strip().split("\t")[1] for x in data}
    return names


@file_opener
def process_data_content(file):
    content = file.read()
    icon_sizes = get_resolutions(content, "Resoluciones")
    icon_names = get_names(content, "Nombres")
    return icon_sizes, icon_names


def get_icon_name(icon_name, icon_names):
    if icon_name in icon_names:
        return icon_names[icon_name]
    return icon_name


def process_png(path, icon_sizes, icon_names):
    img = Image.open(path)
    name = get_icon_name(path[:-4], icon_names)
    img.save(name + ".ico", sizes=icon_sizes, bitmap_format="bmp")
    logger.log(f"Archivo {path} salvado como {name}.ico", "MSG")
    move_file(path, f"png\\{path}")


def main():
    create_folder(
        "png",
        lambda path: logger.log(f"Carpeta {path} creada", "MSG"),
        lambda path: logger.log(f"Carpeta {path} ya existe", "MSG")
    )

    icon_sizes, icon_names = process_data_content(DATA_FILE, Logger)

    file_list = [x for x in os.listdir() if ".png" in x]
    if len(file_list) == 0:
        logger.log("No hay archivos png", "WAR")

    for archivo in file_list:
        process_png(archivo, icon_sizes, icon_names)


if __name__ == "__main__":
    logger = Logger(LOG_FILE)
    logger.log("Starting", "MSG")
    main()
    logger.log("End", "MSG")
