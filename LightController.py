# =============================================================================
# Title: Light Controller
# Author: Ryan J. Slater
# Date: Mon Nov 12 17:48:08 2018
# =============================================================================


import serial
import time
from PIL import Image
import os


def connectToArduino():
    global ser
    ser = None
    for i in range(100):
        try:
            ser = serial.Serial('/dev/ttyACM' + str(i), 115200)
            print('Connected to ttyACM' + str(i))
            time.sleep(2)
            return True
        except:
            pass
    print('Connection failed')
    return False


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

            #singleLineData += ''
            #singleLineData += '@'
            #singleLineData += 'y'
            #wheee!
            singleLineData += str(chr(min(pixelColor[0]//2, 127)))
            singleLineData += str(chr(min(pixelColor[1]//2, 127)))
            singleLineData += str(chr(min(pixelColor[2]//2, 127)))
        lines.append(singleLineData)
        print(singleLineData)
    os.remove(file)
    im.save('imageQueue/currentImage.png')
    return lines


if __name__ == '__main__':
    ser = None
    count = 0

    if connectToArduino():
        time.sleep(2)
        data = arrayFromFile('imageQueue/currentImage.png')
        while True:
            for row in range(len(data)):
                print('Checking for image (' + str(count) + ')')
                images = next(os.walk(os.path.dirname(os.path.realpath(__file__)) + '/imageQueue'))[2]
                print('Collected images')
                count += 1
                if count > 1000:
                    count = 0
                if len(images) > 1:
                    print('Found new image')
                    ser.close()
                    print('Serial port has been closed')
                    images.sort()
                    print('Images sorted')
                    for i in range(len(images)):
                        if images[i] == 'currentImage.png':
                            images.pop(i)
                            break
                    print('Old image removed')
                    print('Loading ' + images[0])
                    data = arrayFromFile('imageQueue/' + images[0])
                    print('Data array for new image collected')
                    connectToArduino()
                    time.sleep(2)
                    print('Running new image...')
                    break
                print('Col loop...')
                ser.write(data[row].encode('ascii'))
                time.sleep(0.02)
        ser.close()
