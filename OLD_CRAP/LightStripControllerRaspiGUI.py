# =============================================================================
# Title: Light Strip Controller Raspi GUI
# Author: Ryan J. Slater
# Date: Sat Nov 10 00:36:22 2018
# =============================================================================

import pygame
import time
import os
from shutil import copyfile
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def buttonImage(x, y, w, h, ic, ac, display, action=None, param=None):
    pygame.font.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        display.blit(ac, (x, y))
        if click[0] == 1 and action is not None:
            if param is None:
                action()
            else:
                action(param)
    else:
        display.blit(ic, (x, y))


def sendImage(image):
    copyfile('images/' + image, 'imageQueue/' + image)

def changeCurrentImage(amount):
    global images
    global imageThumbs
    global currentIndex
    currentIndex += amount
    if currentIndex < 0:
        currentIndex = len(imageThumbs) - 4
    elif currentIndex >= len(imageThumbs) - 1:
        currentIndex = 0
    time.sleep(0.2)
    print(currentIndex)


def LightStripControllerGUI():
    global images
    global imageThumbs
    global currentIndex
    global thumbWidth, thumbHeight
    leftInactive = pygame.transform.scale(pygame.image.load('textures/leftInactive.png'), (displayWidth//10, displayHeight))
    leftActive = pygame.transform.scale(pygame.image.load('textures/leftActive.png'), (displayWidth//10, displayHeight))
    rightInactive = pygame.transform.scale(pygame.image.load('textures/rightInactive.png'), (displayWidth//10, displayHeight))
    rightActive = pygame.transform.scale(pygame.image.load('textures/rightActive.png'), (displayWidth//10, displayHeight))

    currentIndex = 0
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # L/R arrows
        buttonImage(0, 0, displayWidth//10, displayHeight, leftInactive, leftActive, window, changeCurrentImage, -4)
        buttonImage(displayWidth - (displayWidth//10), 0, displayWidth//10, displayHeight, rightInactive, rightActive, window, changeCurrentImage, 4)

        # Thumbnails

        # Top left
        buttonImage(displayWidth//10, 0, thumbWidth, thumbHeight, imageThumbs[currentIndex][0], imageThumbs[currentIndex][0], window, sendImage,  imageThumbs[currentIndex][1])
        # Top right
        buttonImage(displayWidth//10 + thumbWidth, 0, thumbWidth, thumbHeight, imageThumbs[currentIndex+1][0], imageThumbs[currentIndex+1][0], window, sendImage, imageThumbs[currentIndex+1][1])
        # Bottom left
        buttonImage(displayWidth//10, thumbHeight, thumbWidth, thumbHeight, imageThumbs[currentIndex+2][0], imageThumbs[currentIndex+2][0], window, sendImage, imageThumbs[currentIndex+2][1])
        # Bottom right
        buttonImage(displayWidth//10 + thumbWidth, thumbHeight, thumbWidth, thumbHeight, imageThumbs[currentIndex+3][0], imageThumbs[currentIndex+3][0], window, sendImage, imageThumbs[currentIndex+3][1])

        clock.tick(30)
        if counter % 3 == 0:
            pygame.display.update()
        counter += 1


if __name__ == '__main__':
    pygame.init()
    displayWidth = 480
    displayHeight = 320
    thumbWidth = 2*displayWidth//5
    thumbHeight = displayHeight//2
    DEBUG = False

    window = None
    if DEBUG:
        window = pygame.display.set_mode((displayWidth, displayHeight))
    else:
        window = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    #Load the image paths
    images = next(os.walk('images'))[2]
    images.sort()

    imageThumbs = []

    #Load every image in the file
    for file in images:
        imageThumbs.append((pygame.transform.scale(pygame.image.load('images/' + file), (thumbWidth, thumbHeight)), file))

    #Pad with dummy images
    while len(imageThumbs) % 4:
        imageThumbs.append((pygame.transform.scale(pygame.image.load('images/' + images[0]), (thumbWidth, thumbHeight)), images[0]))

    LightStripControllerGUI()
