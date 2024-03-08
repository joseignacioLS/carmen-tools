import os
import re
from PIL import Image
from tools.logger import Logger
from tools.commandline import getargs
from utils import get_content_section, generate_ico_layer
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

    @getargs
    def main(self, args):
        create_folder(
            "png",
            lambda path: self.logger.log(f"Carpeta {path} creada", "MSG"),
            lambda path: self.logger.log(f"Carpeta {path} ya existe", "MSG")
        )

        self.get_file_list()
        if args.get("-m") in [None, "c", "convert"]:
            self.logger.log("Conversión de PNG a ICO", "MSG")
            for archivo in self.file_list:
                self.process_png(archivo)
        elif args.get("-m") in ["f", "fuse"]:
            self.fuse_pngs()
        self.logger.log("End", "MSG")

    @get_content_section
    def get_resolutions(self, data):
        try:
            high = []
            low = []
            switch = False
            for row in data:
                if row == "-":
                    switch = True
                    continue
                if switch:
                    low.append((int(row), int(row)))
                else:
                    high.append((int(row), int(row)))

            resolutions = [high, low]
        except ValueError:
            self.logger.log("Formato incorrecto en las resoluciones", "ERR")
            sys.exit()
        if len(resolutions) == 0:
            self.logger.log("No existen resoluciones", "ERR")
            sys.exit()
        self.icon_sizes = resolutions

    @get_content_section
    def get_names(self, data):
        try:
            names = {x.strip().split("\t")[0]: x.strip().split("\t")[1] for x in data}
            self.icon_names = names
        except IndexError:
            self.logger.log("Formato incorrecto en los nombres", "ERR")
            sys.exit()

    @file_reader
    def process_data_content(self, content):
        clean_content = re.sub(r"\n+", "\n", content).strip()
        self.get_resolutions(content=clean_content, section="Resoluciones")
        self.get_names(content=clean_content, section="Nombres")

    def get_config(self, data_file):
        if file_exists(data_file):
            self.logger.log("Cargando Configuracion Local", "MSG")
            self.process_data_content(data_file=data_file)
        else:
            self.logger.log("No Existe Configuración Local", "WRN")
            path = os.path.abspath(sys.argv[0])
            global_config_path = os.path.join(os.path.dirname(path), data_file)
            if not file_exists(global_config_path):
                self.logger.log(
                    "No Existe Configuración Global. "
                    "Añade un archivo config.txt en la misma localización que el ejecutable.",
                    "ERR")
                sys.exit()
            self.process_data_content(data_file=global_config_path)

    def fuse_pngs(self):
        self.logger.log("Fusión de PNGs a ICO", "MSG")

        fs16, fs32 = [
            [f for f in self.file_list
             if "_16" in f],
            [f for f in self.file_list
             if "_32" in f]]

        sizes_h = [(64, 64), (32, 32), (24, 24)]\
            if len(self.icon_sizes[0]) == 0\
            else self.icon_sizes[0]

        sizes_l = [(16, 16)]\
            if len(self.icon_sizes[1]) == 0\
            else self.icon_sizes[1]

        for f16, f32 in zip(fs16, fs32):
            self.combine_pngs_into_ico([
                {
                    "src": f32,
                    "sizes": sizes_h
                },
                {
                    "src": f16,
                    "sizes": sizes_l
                }
            ])
            move_file(f16, f"png\\{f16}")
            move_file(f32, f"png\\{f32}")

    def process_png(self, path):
        img = Image.open(path)
        img = img.resize(self.icon_sizes[0][0])
        name = self.get_icon_name(path[:-4])
        img.save(f"{name}.ico", sizes=self.icon_sizes[0] + self.icon_sizes[1], bitmap_format="bmp")
        self.logger.log(f"Archivo {path} salvado como {name}.ico", "MSG")
        move_file(path, f"png\\{path}")

    def combine_pngs_into_ico(self, image_data):
        layers = []
        sizes = []
        f_name = None
        for data in image_data:
            if f_name is None:
                f_name = data["src"].split("_")[0]
            img = Image.open(data["src"])
            for size in data["sizes"]:
                sizes.append(size)
                layers.append(generate_ico_layer(img, size))
        icon_name = self.get_icon_name(f_name)
        layers[0].save(f"{icon_name}.ico", bitmap_format="bmp", sizes=sizes, append_images=layers[1:])

    def get_icon_name(self, icon_name):
        if icon_name in self.icon_names:
            return self.icon_names[icon_name]
        return icon_name


if __name__ == "__main__":
    converter = PngToIcoConverter(DATA_FILE, LOG_FILE)
    converter.main()
