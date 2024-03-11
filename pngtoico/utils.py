import re
from PIL import Image


def get_content_section(func):
    def get_content_lines(content):
        return content.strip().split("\n")[1:]

    def wrap(*args, **kwargs):
        match = re.search(f"#{kwargs['section']}[^#]+", kwargs['content'])
        return func(*args, get_content_lines(match.group()) if match else None)

    return wrap


def generate_ico_layer(img, size):
    img = img.resize(size).convert("RGBA")
    ico_layer = Image.new("RGBA", size, (255, 255, 255, 0))
    ico_layer.paste(img, (0, 0))
    return ico_layer


def sort_resolutions(res):
    return sorted(res, key=lambda x: x[0], reverse=True)
