# =============================================================================
# Title: Light Strip Controller Raspi GUI
# Author: Ryan J. Slater
# Date: Sat Nov 10 00:36:22 2018
# =============================================================================

import pygame
import time
import os
from shutil import copyfile


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
    global currentIndex
    currentIndex += amount
    if currentIndex < 0:
        currentIndex = len(images) - 1
    elif currentIndex >= len(images):
        currentIndex = 0
    time.sleep(0.2)


def LightStripControllerGUI():
    global images
    global currentIndex
    global dirPath
    dirPath = os.path.dirname(os.path.realpath(__file__))
    leftInactive = pygame.transform.scale(pygame.image.load(dirPath + '/textures/leftInactive.png'), (displayWidth//10, displayHeight))
    leftActive = pygame.transform.scale(pygame.image.load(dirPath + '/textures/leftActive.png'), (displayWidth//10, displayHeight))
    rightInactive = pygame.transform.scale(pygame.image.load(dirPath + '/textures/rightInactive.png'), (displayWidth//10, displayHeight))
    rightActive = pygame.transform.scale(pygame.image.load(dirPath + '/textures/rightActive.png'), (displayWidth//10, displayHeight))

    images = next(os.walk(dirPath + '/images'))[2]
    images.sort()

    currentIndex = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        buttonImage(0, 0, displayWidth//10, displayHeight, leftInactive, leftActive, window, changeCurrentImage, -1)
        buttonImage(displayWidth - (displayWidth//10), 0, displayWidth//10, displayHeight, rightInactive, rightActive, window, changeCurrentImage, 1)

        currentImage = pygame.transform.scale(pygame.image.load(dirPath + '/images/' + images[currentIndex]), (4*displayWidth//5, displayHeight))
        buttonImage(displayWidth//10, 0, 4*displayWidth//5, displayHeight, currentImage, currentImage, window, sendImage, images[currentIndex])

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    displayWidth = 480
    displayHeight = 320
    DEBUG = False

    window = None
    if DEBUG:
        window = pygame.display.set_mode((displayWidth, displayHeight))
    else:
        window = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    LightStripControllerGUI()
