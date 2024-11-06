# imports
import pygame, sys
from pygame.locals import *

# canvas variables
WIDTH = 800
HEIGHT = 600
FRAME_SIZE = 128

# initializing pygame, setting up the surface (canvas)
pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pine Tree Catacombs!!!")

# import assets
santa_sley = pygame.image.load("santa_sley.png").convert()
santa_sley_list = []

# load sprite sheet into list
TOTAL_SPRITES = 2
for i in range(TOTAL_SPRITES):
    rect = pygame.Rect(TOTAL_SPRITES * FRAME_SIZE, 0, FRAME_SIZE, FRAME_SIZE)
    image = santa_sley.subsurface(rect)
    santa_sley_list.append(image)

# variable to control state of entire game
running = True

# animation variables
SPRITE_COUNTER = 0

# game loop - poll events until window is closed out
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    canvas.blit(santa_sley_list[0], (0, 0))
    pygame.display.update()