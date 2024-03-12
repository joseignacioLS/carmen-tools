import os
import re
from PIL import Image
from tools.logger import Logger
from utils import get_content_section, generate_ico_layer, sort_resolutions
from tools.fs import file_reader, create_folder, move_file, file_exists, get_files_in_path
from contants import LOG_FILE, DATA_FILE, LOW_SUFFIX, HIGH_SUFFIX
import sys


class PngToIcoConverter:
    def __init__(self, data_file, log_file_path):
        self.logger = Logger(log_file_path)

        self.icon_names = {}
        self.icon_sizes = []
        self.get_config(data_file)

        self.file_list = []
        self.get_file_list()

    @get_content_section
    def get_resolutions(self, data):
        if data is None:
            self.logger.log("No existe sección de resoluciones en el archivo de configuracion", "ERR")
            sys.exit()
        try:
            if "-" in data:
                self.icon_sizes = [sort_resolutions([(int(x), int(x)) for x in group.split(";")])
                                   for group in ";".join(data).split(";-;")]
            else:
                self.icon_sizes = [sort_resolutions([(int(x), int(x)) for x in data]), []]
            if len(self.icon_sizes[0]) == 0:
                self.logger.log("El grupo de altas resoluciones no puede estar vacio", "ERR")
                sys.exit()
        except ValueError:
            self.logger.log("Formato incorrecto en las resoluciones", "ERR")
            sys.exit()

    @get_content_section
    def get_names(self, data):
        if data is None:
            self.logger.log("No existe sección de nombres en el archivo de configuración", "MSG")
            return
        try:
            names = {x.strip().split("\t")[0]: x.strip().split("\t")[1] for x in data}
            self.icon_names = names
        except IndexError:
            self.logger.log("Formato incorrecto en los nombres", "ERR")
            sys.exit()

    @file_reader
    def process_data_content(self, content):
        if content is None:
            self.logger.log("Archivo no encontrado", "WAR")
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
            self.logger.log("Cargando Configuracion Global", "MSG")
            if not file_exists(global_config_path):
                self.logger.log(
                    "No Existe Configuración Global. "
                    "Añade un archivo config.txt en la misma localización que el ejecutable.",
                    "ERR")
                sys.exit()
            self.process_data_content(data_file=global_config_path)

    def get_icon_name(self, icon_name):
        if icon_name in self.icon_names:
            return self.icon_names[icon_name]
        return icon_name

    def process_png(self, path):
        img = Image.open(path)
        base_res = self.icon_sizes[0][0]
        img = img.resize(base_res)
        name = self.get_icon_name(path[:-4])
        img.save(f"{name}.ico", sizes=self.icon_sizes[0] + self.icon_sizes[1], bitmap_format="bmp")
        self.logger.log(f"Archivo {path} salvado como {name}.ico", "MSG")

    def combine_pngs_into_ico(self, files):
        layers = []
        sizes_arr = []
        f_name = None
        for src, sizes in zip(files, self.icon_sizes):
            if f_name is None:
                f_name = src.split("_")[0]
            img = Image.open(src)
            for size in sizes:
                sizes_arr.append(size)
                layers.append(generate_ico_layer(img, size))

        icon_name = self.get_icon_name(f_name)
        layers[0].save(f"{icon_name}.ico", bitmap_format="bmp", sizes=sizes_arr, append_images=layers[1:])
        self.logger.log(f"Archivos {files[0]} y {files[1]} salvados como {icon_name}.ico", "MSG")

    def get_file_list(self, ):
        self.file_list = []
        png_files = sorted(get_files_in_path(".", "png"))

        if len(png_files) == 0:
            self.logger.log("No hay archivos png", "WAR")
            sys.exit()

        cache = []

        for path in png_files:
            if LOW_SUFFIX in path or HIGH_SUFFIX in path:
                high_path = path.replace(LOW_SUFFIX, HIGH_SUFFIX)
                low_path = path.replace(HIGH_SUFFIX, LOW_SUFFIX)
                if file_exists(high_path) and file_exists(low_path):
                    if high_path in cache or low_path in cache:
                        continue
                    self.file_list.append([high_path, low_path])
                    cache += [high_path, low_path]
                else:
                    self.logger.log(f"Error con la pareja {high_path} / {low_path}", "WAR")
            elif path not in cache:
                self.file_list.append([path])
                cache += path

    def main(self):
        create_folder(
            "png",
            lambda x: self.logger.log(f"Carpeta {x} creada", "MSG"),
            lambda x: self.logger.log(f"Carpeta {x} ya existe", "MSG")
        )

        for file in self.file_list:
            if len(file) == 1:
                self.process_png(file[0])
            elif len(file) == 2:
                self.combine_pngs_into_ico(file)
            for path in file:
                move_file(path, f"png\\{path}")

        self.logger.log("End", "MSG")


if __name__ == "__main__":
    converter = PngToIcoConverter(DATA_FILE, LOG_FILE)
    converter.main()
