# imports
import pygame, sys
from pygame.locals import *

# canvas variables
WIDTH = 800
HEIGHT = 600

# initializing pygame, setting up the surface (canvas)
pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pine Tree Catacombs!!!")

# initialize joystick
pygame.joystick.init()
joysticks = []

# import assets
santa_sley = pygame.image.load("santa_sley.png").convert_alpha()
TOTAL_SPRITES = 3
sprite_sheet_width = santa_sley.get_rect().width
sprite_sheet_height = santa_sley.get_rect().height

# transform sprite sheet size
scale_size = 1.5
sprite_sheet_width = sprite_sheet_width * scale_size
sprite_sheet_height = sprite_sheet_height * scale_size
santa_sley = pygame.transform.scale(santa_sley, (sprite_sheet_width, sprite_sheet_height))
sprite_sheet_width = santa_sley.get_rect().width
sprite_sheet_height = santa_sley.get_rect().height
SPRITE_WIDTH = sprite_sheet_width // 3
SPRITE_HEIGHT = sprite_sheet_width // 3
santa_sley_list = []

# santa's position
santa_sley_x = 0
santa_sley_y = 0

# load sprite sheet into list
for i in range(TOTAL_SPRITES):
    rect = pygame.Rect(i * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
    image = santa_sley.subsurface(rect)
    santa_sley_list.append(image)

# variable to control state of entire game
running = True

# sprite picker function for animation
sprite_index = 0
def spritePicker():
    global sprite_index
    if sprite_index == TOTAL_SPRITES - 1:
        sprite_index = 0
    else:
        sprite_index += 1

# clock to set FPS
clock = pygame.time.Clock()

# game loop - poll events until window is closed out
while running:
    # paint canvas
    canvas.fill((207, 207, 230))

    # event handler
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)

        if joysticks[0].get_button(2):
            santa_sley_x += 5

    canvas.blit(santa_sley_list[sprite_index], (santa_sley_x, santa_sley_y))
    spritePicker()
    pygame.display.update()
    clock.tick(10)