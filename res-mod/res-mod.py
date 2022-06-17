from os import listdir
from PIL import Image
from math import floor

SUPPORTED_TYPES = ["jpg","png","jpeg"]

TAG = "_tag"

newWidth = int(input("Output width: "))

imageFiles = [file for file in listdir() if file.split(".")[-1] in SUPPORTED_TYPES and TAG not in file]

for file in imageFiles:
    name, format = file.split(".")
    im = Image.open(file)
    size = im.size

    modRes = (newWidth, floor(size[1] * newWidth / size[0]))

    resizedIm = im.resize(modRes)
    resizedIm.save(name+TAG+"."+format)

