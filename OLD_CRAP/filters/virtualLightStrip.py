#!/usr/bin/env python
import pygame
from pygame.locals import *
from imagestream import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size, IS_FULLSCREEN * pygame.FULLSCREEN)
    pygame.display.set_caption("Virtual Light Strips")
    clock = pygame.time.Clock()

    # Set up the image reader
    fifo = open('picture.fifo', 'r')
    print(fifo.readline())
    stream = ImageStream(inputStream=lambda: fifo.readline().rstrip())
    stream.begin()

    while True:
        clock.tick(FPS)
        pygame.event.pump()
        keystate = pygame.key.get_pressed()

        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            break


        screen.fill((000, 000, 000))
        
        line = stream.getNextLine()
        
        for i in range(300):
            pygame.draw.circle(screen, line.data[i], (i*5+3, 3), 2, 2)
        
        pygame.display.update()

if __name__ == '__main__':
    SCREEN_SIZE = Rect(0, 0, 300 * 5 + 1, 7)
    IS_FULLSCREEN = 0
    FPS = 15
    main()
