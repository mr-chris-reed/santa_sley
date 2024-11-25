# imports
import pygame, random, sys
from pygame.locals import *

# initialize pygame
pygame.init()

# canvas variables
WIDTH = 1920
HEIGHT = 1000

# scoring variables
trees_passed = 0
trees_hit = 0

# font
font = pygame.font.Font('VT323-Regular.ttf', 50)
text_trees_hit = font.render('Trees Hit: ' + str(trees_hit), True, (0, 0, 0))
text_trees_hit.set_alpha(127)
text_trees_hit_rect = text_trees_hit.get_rect()
text_trees_hit_rect.center = (WIDTH - WIDTH // 9, HEIGHT // 12)
text_trees_passed = font.render('Trees Passed: ' + str(trees_passed), True, (0, 0, 0))
text_trees_passed.set_alpha(127)
text_trees_passed_rect = text_trees_hit.get_rect()
text_trees_passed_rect.center = (WIDTH - WIDTH // 8, HEIGHT // 20)

# initializing pygame, setting up the surface (canvas)
pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pine Tree Catacombs!!!")

# initialize joystick
pygame.joystick.init()
joysticks = []
count = 1

# import assets
santa_sley = pygame.image.load("santa_sley.png").convert_alpha()
TOTAL_SPRITES = 3
sprite_sheet_width = santa_sley.get_rect().width
sprite_sheet_height = santa_sley.get_rect().height
pine_tree = pygame.image.load("holiday_tree.png").convert_alpha()
pine_tree_sprite_width = pine_tree.get_rect().width
pine_tree_sprite_height = pine_tree.get_rect().height

# transform sprite sheet size
scale_size = 2.0
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

# pine trees
class PineTree():

    def __init__(self, flip):
        self.scale = random.randint(2, 6)
        self.pine_tree = pygame.image.load("holiday_tree.png").convert_alpha()
        if flip:
            self.pine_tree = pygame.transform.rotate(self.pine_tree, 180)
        self.pine_tree_sprite_width = pine_tree_sprite_width * self.scale
        self.pine_tree_sprite_height = pine_tree_sprite_height * self.scale
        self.pine_tree = pygame.transform.scale(self.pine_tree, (self.pine_tree_sprite_width, self.pine_tree_sprite_height))
        self.pine_tree_x = WIDTH
        self.pine_tree_y = HEIGHT - self.pine_tree_sprite_height
        self.rect = pygame.Rect(0, 0, self.pine_tree_sprite_width, self.pine_tree_sprite_height)
        self.image = self.pine_tree.subsurface(self.rect)
        self.wasHit = False
        self.successfullyPassed = False

    def moveLeft(self):
        self.pine_tree_x -= 5

    def moveTreeToTop(self):
        self.pine_tree_y = 0

pine_trees_bottom = []
pine_trees_top = []

# variable to control state of entire game
running = True

# sprite picker function for animation
sprite_index = 0
counter = 0
def spritePicker():
    global counter, sprite_index
    if counter % 20 == 0:
        if sprite_index == TOTAL_SPRITES - 1:
            sprite_index = 0
        else:
            sprite_index += 1

def checkToAddAnotherTree(pt, flip):
    if (counter % 90) == 0 and not(flip):
        new_pine_tree = PineTree(flip)
        pt.append(new_pine_tree)
    elif ((counter + 60) % 90) == 0 and flip:
        new_pine_tree = PineTree(flip)
        new_pine_tree.moveTreeToTop()
        pt.append(new_pine_tree)

def checkIfPineTreeCanBeRemoved(pt):
    i = 0
    while i < len(pt):
        if pt[i].pine_tree_x + pt[i].pine_tree_sprite_width < 0:
            pt.pop(i)
        else:
            i += 1

def checkForCollisionOnTop(ss, pt):
    ss_hitbox = pygame.Rect((santa_sley_x + 20), (santa_sley_y + 40), SPRITE_WIDTH * 0.8, SPRITE_HEIGHT * 0.5)
    pt_hitbox = pygame.Rect((pt.pine_tree_x + (pt.pine_tree_sprite_width // 2.5)), (pt.pine_tree_y + pt.pine_tree_y // 10), pt.pine_tree_sprite_width * 0.2, pt.pine_tree_sprite_height * 0.87)
    pygame.draw.rect(canvas, (255,0,0), ss_hitbox)
    pygame.draw.rect(canvas, (0,255,0), pt_hitbox) 
    if ss_hitbox.colliderect(pt_hitbox) and pt.wasHit == False:
        pt.wasHit = True
        return True
    return False

def checkForCollisionOnBottom(ss, pt):
    ss_hitbox = pygame.Rect((santa_sley_x + 20), (santa_sley_y + 40), SPRITE_WIDTH * 0.8, SPRITE_HEIGHT * 0.5)
    pt_hitbox = pygame.Rect((pt.pine_tree_x + (pt.pine_tree_sprite_width // 2.7)), (pt.pine_tree_y + pt.pine_tree_sprite_height // 7.5), pt.pine_tree_sprite_width * 0.2, pt.pine_tree_sprite_height * 0.87)
    pygame.draw.rect(canvas, (255,0,0), ss_hitbox)
    pygame.draw.rect(canvas, (0,255,0), pt_hitbox)
    if ss_hitbox.colliderect(pt_hitbox) and pt.wasHit == False:
        pt.wasHit = True
        return True
    return False

def checkIfTreedWasPassed(pt):
    global trees_passed
    if santa_sley_x > pt.pine_tree_x and not(pt.successfullyPassed):
        trees_passed += 1
        pt.successfullyPassed = True


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

    santa_sley_x += joysticks[0].get_axis(0) * 5
    santa_sley_y += joysticks[0].get_axis(1) * 5

     # check for collisions
    for pine_tree_top in pine_trees_top:
        if (checkForCollisionOnTop(santa_sley, pine_tree_top)):
            trees_hit += 1
    for pine_tree_bottom in pine_trees_bottom:
        if (checkForCollisionOnBottom(santa_sley, pine_tree_bottom)):
            trees_hit += 1

    # check for sley passing tree
    for pine_tree_top in pine_trees_top:
        checkIfTreedWasPassed(pine_tree_top)
    for pine_tree_bottom in pine_trees_bottom:
        checkIfTreedWasPassed(pine_tree_bottom)
        

    canvas.blit(santa_sley_list[sprite_index], (santa_sley_x, santa_sley_y))
    checkToAddAnotherTree(pine_trees_bottom, False)
    checkToAddAnotherTree(pine_trees_top, True)

    for pine_tree in pine_trees_bottom:
        pine_tree.moveLeft()
        checkIfPineTreeCanBeRemoved(pine_trees_bottom)
        canvas.blit(pine_tree.image, (pine_tree.pine_tree_x, pine_tree.pine_tree_y))

    for pine_tree in pine_trees_top:
        pine_tree.moveLeft()
        checkIfPineTreeCanBeRemoved(pine_trees_top)
        canvas.blit(pine_tree.image, (pine_tree.pine_tree_x, pine_tree.pine_tree_y))

    text_trees_hit = font.render('Trees Hit: ' + str(trees_hit), True, (0, 0, 0))
    canvas.blit(text_trees_hit, text_trees_hit_rect)

    text_trees_passed = font.render('Trees Passed: ' + str(trees_passed), True, (0, 0, 0))
    canvas.blit(text_trees_passed, text_trees_passed_rect)

    spritePicker()
    pygame.display.update()
    counter += 1
    clock.tick(60)