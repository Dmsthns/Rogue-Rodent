#! /usr/bin/env python

#Rogue Rodent test code, mainly co-opted with sources from other platformers
#and the source code from Plaoo on making a 2d platformer
#For the use of testing and demonstration of ideas
#Definitely should be improved/changed

import pygame
from pygame.locals import *
import sys

#Set the stage
SCREEN_SIZE = (1280, 720) #resolution of the game
global HORIZ_MOV_INCR #speed of movement
HORIZ_MOV_INCR = 10

#Game logistics
global FPS
global clock
global time_spent

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)


class Camera(object):
    #Camera class for controlling the view of the player
    #responsible for setting up the player, it's orientation and level parameters
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.scene_rect = Rect(0, 0, level_width, level_height)

    #update method that sets itself to move with the player
    def update(self):
      if self.player.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.player.centerx - 25
      if self.player.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.player.centerx + 25
      if self.player.centery > self.rect.centery + 25:
          self.rect.centery = self.player.centery - 25
      if self.player.centery < self.rect.centery - 25:
          self.rect.centery = self.player.centery + 25
      self.rect.clamp_ip(self.scene_rect)

    #Draws all of the sprites in the landscape
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


class Obstacle(pygame.sprite.Sprite):
    #Creates a block that can be collided with
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/obstacle.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


class CheeseCollected(pygame.sprite.RenderClear):
    '''
        A RenderClear Group object containing the cheese collected so its clear method can undraw the cheese. TZ
    '''
    def __init__(self):
        pygame.sprite.RenderClear__init__(self)


class Cheese(pygame.sprite.Sprite):
    #Creates a cheese block that when collided with, tells the rodent he's got cheese
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/cheesetest.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        #need to create something that will undraw the cheese when it's taken!
        #TZ 
        self.collected = False  #This checks to see if the cheese has been collected
        self.undrawn = False #This checks to see if the cheese has undrawn so that it doesn't try to undraw multiple times
        if self.collected == True and self.undrawn == False:
            collected = CheeseCollected()
            collected.add(self)
            collected.clear()
            self.mouseHas()
            self.undrawn = True
        
    def setCollected(self, answer):
        '''
            Changes self.collected to answer to indicate whether it's been collected. TZ
        '''
        self.collected = answer

    def getCollected(self):
        '''
            Returns a Boolean for whether the rodent has the cheese. TZ
        '''
        return self.collected

class Goal(pygame.sprite.Sprite):
    #Creates the exit
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/goal.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        

class Rogue(pygame.sprite.Sprite):
    #Controls the player and their collisions
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contact = False
        self.jump = False
        self.hasCheese = False #boolean that shows the cheese has been obtained
        #set to mouse symbol
        if self.hasCheese == True:
            self.image = pygame.image.load('actions/rodentC.png').convert()
            #TZ
            font = pygame.font.SysFont("Times New Roman", 21, bold=True)
            text = font.render("Cheese!", True, (0, 0, 0))
            screen.blit(text,(10, 10)) #Need to experiment with the coordinates to figure out where to blit it. Also, can we change the color? Couldn't find anything

        else:
            self.image = pygame.image.load('actions/rodent.png').convert()
        self.rect = self.image.get_rect()

        #no animations, so the mouse symbol will stay static
        self.run_left = ["actions/rodent.png"]
        #                  "actions/run_left002.png", "actions/run_left003.png",
        #                  "actions/run_left004.png", "actions/run_left005.png",
        #                  "actions/run_left006.png", "actions/run_left007.png"]
        self.run_right = ["actions/rodent.png"]
        #                  "actions/run_right002.png", "actions/run_right003.png",
        #                  "actions/run_right004.png", "actions/run_right005.png",
        #                  "actions/run_right006.png", "actions/run_right007.png"]
        #starting direction
        self.direction = "right"
        self.rect.topleft = [x, y]
        #setting frames if using an animation
        self.frame = 0

    def mouseHas(self, screen):
        '''
            Creates the cheese icon. Redundant, I'll fix it once I can see what works TZ
        '''
        font = pygame.font.SysFont("Times New Roman", 21, bold=True)
        text = font.render("Cheese!", True, (0, 0, 0))
        screen.blit(text,(10, 10)) #Need to experiment with the coordinates to figure out where to blit it. Also, can we change the color? Couldn't find anything

    #update information for the player, depending on input
    def update(self, up, down, left, right):
        if up: #if input = up
            if self.contact: #in contact with self
                self.jump = True #he jumps
                self.movy -= 20
        if down:
            #crouching would go here
            if self.contact and self.direction == "right":
                self.image = pygame.image.load('actions/rodent.png').convert_alpha()
            if self.contact and self.direction == "left":
                self.image = pygame.image.load('actions/rodent.png').convert_alpha()

        if not down and self.direction == "right":
                self.image = pygame.image.load('actions/rodent.png').convert_alpha()

        if not down and self.direction == "left":
            self.image = pygame.image.load('actions/rodent.png').convert_alpha()

        if left:
            self.direction = "left"
            self.movx = -HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                #animation by frame
                self.image = pygame.image.load('actions/rodent.png').convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("actions/rodent.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                #animation by frame
                self.image = pygame.image.load('actions/rodent.png').convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = self.image = pygame.image.load("actions/rodent.png").convert_alpha()

        if not (left or right):
            self.movx = 0
        
        self.rect.right += self.movx
        self.collide(self.movx, 0, scene)
        #TZ
        if self.hasCheese == True:
            self.mouseHas(screen)
                

        if not self.contact:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.jump:
            self.movy += 2
            self.rect.top += self.movy
            if self.contact == True:
                self.jump = False

        self.contact = False
        self.collide(0, self.movy, scene)


    def collide(self, movx, movy, scene):
        #Controls collision
        self.contact = False
        for o in scene:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                if o == Cheese:
                    self.hasCheese = True
                    Cheese.setCollected(True)


class Level(object):
    #reads a map within a txt and creates a level as a result
    def __init__(self, open_level):
        self.level1 = []
        self.scene = []
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                if col == "X":
                    obstacle = Obstacle(x, y)
                    self.scene.append(obstacle)
                    self.all_sprite.add(self.scene)
                if col == "C":
                    cheese = Cheese(x, y)
                    self.scene.append(cheese)
                    self.all_sprite.add(self.scene)
                if col == "G":
                    goal = Goal(x, y)
                    self.scene.append(goal)
                    self.all_sprite.add(self.scene)
                if col == "S":
                    self.Rogue = Rogue(x,y)
                    self.all_sprite.add(self.Rogue)
                x += 25
            y += 25
            x = 0

    def get_size(self):
        lines = self.level1
        #line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)

    def getSprites(self):
        '''
            Returns all the sprites contained in the Group object of the level. TZ
        '''
        return self.scene

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

def getCheese(sprites):
    '''
        Gets the Cheese object from a group sprites and returns it. sprites must have a Cheese object. 
        Written because I can't access the cheese created by the Level class otherwise. TZ
    '''
    for i in range(len(sprites)):
        if type(sprites[i]) == Cheese:
            return sprites[i]


#Starting the game
pygame.init()
#Setting the screen up
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
screen_rect = screen.get_rect()
background = pygame.image.load("scene/background2.jpg").convert_alpha()
background_rect = background.get_rect()
#Setting up and creating the level
level = Level("level/level1")
level.create_level(0,0)
scene = level.scene
Rogue = level.Rogue
pygame.mouse.set_visible(0)

#Setting up the camera
camera = Camera(screen, Rogue.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite

#TZ
sprites = level.getSprites()
cheese = getCheese(sprites)

#Setting frames per second and time
FPS = 60
clock = pygame.time.Clock()

#Controls init
up = down = left = right = False
x, y = 0, 0
while True:

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_UP:
            up = True
        if event.type == KEYDOWN and event.key == K_DOWN:
            down = True
        if event.type == KEYDOWN and event.key == K_LEFT:
            left = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            right = True

        if event.type == KEYUP and event.key == K_UP:
            up = False
        if event.type == KEYUP and event.key == K_DOWN:
            down = False
        if event.type == KEYUP and event.key == K_LEFT:
            left = False
        if event.type == KEYUP and event.key == K_RIGHT:
            right = False

    asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
    bg = pygame.Surface(asize)


    for x in range(0, asize[0], background_rect.w):
        for y in range(0, asize[1], background_rect.h):
            screen.blit(background, (x, y))
            
            #I'm not actually sure where this goes; I just put it here to show that it needs to be in the loop. TZ
            collected = cheese.getCollected()
            if collected == True:
                font = pygame.font.SysFont("Times New Roman", 21, bold=True)
                text = font.render("Cheese!", True, (0, 0, 0))
                screen.blit(text,(10, 10)) #Need to experiment with the coordinates to figure out where to blit it. Also, can we change the color? Couldn't find anything
#We can also add a conditional here to see if collected == True when the rodent makes contact with the goal



    time_spent = tps(clock, FPS)
    camera.draw_sprites(screen, all_sprite)

    Rogue.update(up, down, left, right)
    camera.update()
    pygame.display.flip()
