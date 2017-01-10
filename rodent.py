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

'''
	added a method for each sprite that returns the type of sprite
	this is useful in collisions for determining what object the rogue is touching
'''

class Obstacle(pygame.sprite.Sprite):
    #Creates a block that can be collided with
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/obstacle.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
    
    def getType(self):
    	return 1

class Enemy(pygame.sprite.Sprite):
    #Creates a block that can be collided with
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/floor1.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
    
    def getType(self):
    	return 2

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
    
    def getType(self):
    	return 3

class Goal(pygame.sprite.Sprite):
    #Creates a cheese block that when collided with, tells the rodent he's got cheese
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("scene/goal.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        #need to create something that will undraw the cheese when it's taken!
    
    def getType(self):
    	return 4

'''
	commented out a lot of the image changes to simplify the game's appearance for now
	commented out the entire "down" portion, since we have no use for this key right now
'''

class Rogue(pygame.sprite.Sprite):
    #Controls the player and their collisions
    def __init__(self, x, y, scene):
    	pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.scene = scene
        self.contact = False
        self.jump = False
        self.hasCheese = False #boolean that shows the cheese has been obtained
        self.dead = False
        self.win = False
        #set to mouse symbol
        self.image = pygame.image.load('actions/rodent.png').convert_alpha()
        self.rect = self.image.get_rect()

        #no animations, so the mouse symbol will stay static
#         self.run_left = ["actions/rodent.png"]
        #                  "actions/run_left002.png", "actions/run_left003.png",
        #                  "actions/run_left004.png", "actions/run_left005.png",
        #                  "actions/run_left006.png", "actions/run_left007.png"]
#         self.run_right = ["actions/rodent.png"]
        #                  "actions/run_right002.png", "actions/run_right003.png",
        #                  "actions/run_right004.png", "actions/run_right005.png",
        #                  "actions/run_right006.png", "actions/run_right007.png"]
        #starting direction
        self.direction = "right"
        self.rect.topleft = [x, y]
        #setting frames if using an animation
        self.frame = 0

    #update information for the player, depending on input
    def update(self, up, down, left, right):
    	if self.getHasCheese():
    		self.image = pygame.image.load('actions/rodentC.png').convert_alpha()
    	
        if up: #if input = up
            if self.contact: #in contact with self
                self.jump = True #he jumps
                self.movy -= 20
#         if down:
#             #crouching would go here
#             if self.contact and self.direction == "right":
#                 self.image = pygame.image.load('actions/rodent.png').convert_alpha()
#             if self.contact and self.direction == "left":
#                 self.image = pygame.image.load('actions/rodent.png').convert_alpha()

#         if not down and self.direction == "right":
# 			self.image = pygame.image.load('actions/rodent.png').convert_alpha()

#         if not down and self.direction == "left":
#             self.image = pygame.image.load('actions/rodent.png').convert_alpha()

        if left:
            self.direction = "left"
            self.movx = -HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                #animation by frame
#                 self.image = pygame.image.load('actions/rodent.png').convert_alpha()
                if self.frame == 6: self.frame = 0
#             else:
#                 self.image = self.image = pygame.image.load("actions/rodent.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                #animation by frame
#                 self.image = pygame.image.load('actions/rodent.png').convert_alpha()
                if self.frame == 6: self.frame = 0
#             else:
#                 self.image = self.image = pygame.image.load("actions/rodent.png").convert_alpha()

        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, self.scene)


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
        self.collide(0, self.movy, self.scene)
        
    def collide(self, movx, movy, scene):
	'''
		added conditions so that the rogue does not collide with enemy, cheese, or goal sprites
		used the getType() methods to determine collisions with certain objects
		modified hasCheese, dead, and win variables
	'''
        #Controls collision
        self.contact = False
        for o in scene:
            if self.rect.colliderect(o):
                if (movx > 0 and o.getType() != 3 and o.getType() != 2 and o.getType() != 4):
                    self.rect.right = o.rect.left
                if (movx < 0 and o.getType() != 3 and o.getType() != 2 and o.getType() != 4):
                    self.rect.left = o.rect.right
                if (movy > 0 and o.getType() != 3 and o.getType() != 2 and o.getType() != 4):
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                if (movy < 0 and o.getType() != 3 and o.getType() != 2 and o.getType() != 4):
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                if o.getType() == 3:
					self.hasCheese = True
					self.scene.remove(o)
                if o.getType() == 2:
                	self.dead = True
                if o.getType() == 4:
                	if self.hasCheese == True:
						self.win = True
						
    def getDead(self):
    	return self.dead
    
    def setDead(self, value):
    	self.dead = value
    
    def getHasCheese(self):
    	return self.hasCheese
    
    def getWin(self):
    	return self.win
    
    def getType(self):
    	return 5

class Level(object):
    #reads a map within a txt and creates a level as a result
    def __init__(self, open_level):
        self.level1 = []
        self.scene = []
        self.cheese = 0
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
                    self.cheese = Cheese(x, y)
                    self.scene.append(self.cheese)
                    self.all_sprite.add(self.scene)
                if col == "E":
                	enemy = Enemy(x,y)
                	self.scene.append(enemy)
                	self.all_sprite.add(self.scene)
                if col == "G":
                    goal = Goal(x, y)
                    self.scene.append(goal)
                    self.all_sprite.add(self.scene)
                if col == "S":
                    self.Rogue = Rogue(x,y, self.scene)
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

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

'''
	created a method that runs an individual level based on a given filename (preferably .txt)
'''

#Setting up and creating the level
def runLevel(levelFile):
	#Starting the game
	pygame.init()
	#Setting the screen up
	screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
	screen_rect = screen.get_rect()
	background = pygame.image.load("scene/background2.jpg").convert_alpha()
	background_rect = background.get_rect()
	
	level = Level(levelFile)
	level.create_level(0,0)
	scene = level.scene
	Rogue = level.Rogue
	pygame.mouse.set_visible(0)

	#Setting up the camera
	camera = Camera(screen, Rogue.rect, level.get_size()[0], level.get_size()[1])
	all_sprite = level.all_sprite

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
			# the following condition allows the user to restart the current level
			if event.type == KEYDOWN and event.key == K_r:
				Rogue.setDead(True)

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

		time_spent = tps(clock, FPS)
		camera.draw_sprites(screen, all_sprite)

		Rogue.update(up, down, left, right)
		camera.update()
		pygame.display.flip()
		
		# if the rogue won the game, exit the level
		if Rogue.getWin():
			return
		
		# if the rogue has the cheese, remove the cheese from the group of sprites
		if Rogue.getHasCheese():
			all_sprite.remove(level.cheese)
		
		# if the rogue died, end the level and run it again
		if Rogue.getDead():
			return runLevel(levelFile)

'''
	main code runs the levels in sequence
'''

runLevel("level/level1.txt")
runLevel("level/level2.txt")
runLevel("level/level3.txt")