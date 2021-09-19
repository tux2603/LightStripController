#!/usr/bin/python3
from PIL import Image
import sys

def arrayFromFile(file):
    print('Loading ' + file)
    im = Image.open(file)
    print(im.width, im.height)
    resizeFactor = 300/im.width
    im = im.resize((300, int(resizeFactor*im.height)))
    print(im.width, im.height)
    lines = []
    for row in range(im.height):
        singleLineData = ''
        for col in range(im.width):
            pixelColor = im.getpixel((col, row))
            singleLineData += "%02X" % pixelColor[0]
            singleLineData += "%02X" % pixelColor[1]
            singleLineData += "%02X" % pixelColor[2]
        lines.append(singleLineData)
        print(singleLineData)
    return lines

if __name__ == '__main__':
    imageName = sys.argv[1] if len(sys.argv) > 1 else 'images/0off.png'

    print("CLEAR")
    print("LOOP")

    im = Image.open(imageName)
    resizeFactor = 300/im.width
    im = im.resize((300, int(resizeFactor*im.height)))
    for row in range(im.height):
        singleLineData = ''
        for col in range(im.width):
            pixelColor = im.getpixel((col, row))
            singleLineData += "%02X" % pixelColor[0]
            singleLineData += "%02X" % pixelColor[1]
            singleLineData += "%02X" % pixelColor[2]
        print(singleLineData)

    print("ENDLOOP")
