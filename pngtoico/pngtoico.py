import os
from PIL import Image
from tools.logger import Logger
from utils import get_content_section
from tools.fs import file_opener, create_folder, move_file
from contants import LOG_FILE, DATA_FILE
import sys


class PngToIcoConverter:
    def __init__(self, data_file, log_file_path):
        self.logger = Logger(log_file_path)
        self.icon_names = {}
        self.icon_sizes = []
        self.file_list = []
        self.process_data_content(data_file=data_file, logger=self.logger)

    def get_file_list(self):
        self.file_list = [x for x in os.listdir() if ".png" in x]
        if len(self.file_list) == 0:
            self.logger.log("No hay archivos png", "WAR")

    def main(self):
        create_folder(
            "png",
            lambda path: self.logger.log(f"Carpeta {path} creada", "MSG"),
            lambda path: self.logger.log(f"Carpeta {path} ya existe", "MSG")
        )

        self.get_file_list()

        for archivo in self.file_list:
            self.process_png(archivo)

        self.logger.log("End", "MSG")

    @get_content_section
    def get_resolutions(self, data):
        resolutions = [(int(x), int(x)) for x in data]
        if len(resolutions) == 0:
            self.logger.log("No existen resoluciones", "ERR")
            sys.exit()
        self.icon_sizes = resolutions

    @get_content_section
    def get_names(self, data):
        names = {x.strip().split("\t")[0]: x.strip().split("\t")[1] for x in data}
        self.icon_names = names

    @file_opener
    def process_data_content(self, file):
        content = file.read()
        self.get_resolutions(content=content, section="Resoluciones")
        self.get_names(content=content, section="Nombres")

    def process_png(self, path):
        img = Image.open(path)
        name = self.get_icon_name(path[:-4])
        img.save(name + ".ico", sizes=self.icon_sizes, bitmap_format="bmp")
        self.logger.log(f"Archivo {path} salvado como {name}.ico", "MSG")
        move_file(path, f"png\\{path}")

    def get_icon_name(self, icon_name):
        if icon_name in self.icon_names:
            return self.icon_names[icon_name]
        return icon_name


if __name__ == "__main__":
    converter = PngToIcoConverter(DATA_FILE, LOG_FILE)
    converter.main()
