import os
import inspect
from PIL import Image
from tools.logger import Logger
from utils import get_content_section
from tools.fs import file_reader, create_folder, move_file, file_exists
from contants import LOG_FILE, DATA_FILE
import sys


class PngToIcoConverter:
    def __init__(self, data_file, log_file_path):
        self.logger = Logger(log_file_path)
        self.icon_names = {}
        self.icon_sizes = []
        self.file_list = []
        self.get_config(data_file)

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

    @file_reader
    def process_data_content(self, content):
        print(content)
        self.get_resolutions(content=content, section="Resoluciones")
        self.get_names(content=content, section="Nombres")

    def get_config(self, data_file):
        if file_exists(data_file):
            self.logger.log("Cargando Configuracion Local", "MSG")
            self.process_data_content(data_file=data_file)
        else:
            self.logger.log("No Existe Configuración Local", "WRN")
            path = os.path.abspath(sys.argv[0])
            self.process_data_content(data_file=os.path.join(os.path.dirname(path), data_file))

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
