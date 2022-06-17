from os import listdir
import PIL
from PIL import Image
from math import floor

PIL.Image.MAX_IMAGE_PIXELS = 933120000

SUPPORTED_TYPES = ["jpg","png","jpeg"]

TAG = "_resized"

print("Supported formats: "+", ".join(SUPPORTED_TYPES))

newWidth = int(input("Output width: "))

imageFiles = [file for file in listdir(".") if file.split(".")[-1] in SUPPORTED_TYPES and TAG not in file]
for file in imageFiles:
    try:
        print(f'processing file {file}')
        name, format = file.split(".")
        im = Image.open(file)
        size = im.size

        modRes = (newWidth, int(floor(size[1] * newWidth / size[0])))

        resizedIm = im.resize(modRes)
        resizedIm.save(name+TAG+"."+format)
        print(f'image resized')
    except:
        print(f'error processing the image')

input()