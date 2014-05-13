#!/usr/bin/env python
# Core stuff
import random, math
# Pygame
import pygame
from pygame import *


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, enemytype, playablerect):
        pygame.sprite.Sprite.__init__(self)
        # Load image
        self.image = enemytype.image
        self.rect = self.image.get_rect()
        
        # Generate random spawn
        startLine = random.randint(0,3)
        if(startLine == 0):
            startY = playablerect.top-self.rect.height
            startX = random.randint(playablerect.left, playablerect.right)
        if(startLine == 2):
            startY = playablerect.bottom
            startX = random.randint(playablerect.left, playablerect.right)
        if(startLine == 1):
            startX = playablerect.right
            startY = random.randint(playablerect.top, playablerect.bottom)
        if(startLine == 3):
            startX = playablerect.left-self.rect.width
            startY = random.randint(playablerect.top, playablerect.bottom)
            
        # Update position (and accurate position) to random spawn
        self.rect.x = startX
        self.rect.y = startY
        self.accuratex = startX
        self.accuratey = startY
        
        # Enemy stats
        self.movement = enemytype.movement

        # Store update function
        self.updatefunc = enemytype.updatefunc

        # Run init function
        if(enemytype.initfunc): enemytype.initfunc(self)
        
    def update(self, game):
        self.updatefunc(self, game)

# Update functions for each enemy type
def DefaultEnemyUpdate(self, game):
    playablerect = game.GetPlayableRect()
        
    # Work out the difference in position between the enemy and the player
    DIFFX = game.cage.rect.x - self.rect.x
    DIFFY = game.cage.rect.y - self.rect.y
    DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
    if(DISTANCE < self.movement):
        self.accuratex = game.cage.rect.x
        self.accuratey = game.cage.rect.y
    elif(DIFFX == 0):
        self.accuratey += math.copysign(self.movement, DIFFY)
    elif(DIFFY == 0):
        self.accuratex += math.copysign(self.movement, DIFFX)
    else:
        self.accuratex += self.movement * (DIFFX/DISTANCE)
        self.accuratey += self.movement * (DIFFY/DISTANCE)
        
    # Actually move the sprite. We truncate the more accurate versions of their coordinates
    self.rect.x = int(self.accuratex)
    self.rect.y = int(self.accuratey)

def YoutubeReviewerInit(self):
    self.lastenemyspawn = 0
    self.cagedistance = 320
    self.targetx = -1
    self.targety = -1
    
def YoutubeReviewerUpdate(self, game):
    playablerect = game.GetPlayableRect()
        
    # Work out the difference in position between the enemy and the player
    DIFFX = game.cage.rect.x - self.rect.x
    DIFFY = game.cage.rect.y - self.rect.y
    DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
    if(not playablerect.contains(self.rect)):
        if(self.rect.x < playablerect.left):
            self.accuratex += self.movement
        elif(self.rect.x + self.rect.width > playablerect.right):
             self.accuratex -= self.movement
        if(self.rect.y < playablerect.top):
             self.accuratey += self.movement
        elif(self.rect.y + self.rect.height > playablerect.bottom):
             self.accuratey -= self.movement
    elif(DISTANCE <= self.cagedistance):
        # Reset random target position
        self.targetx = -1
        self.targety = -1
        # Move away from cage
        if(DIFFX == 0):
            newy = self.accuratey + math.copysign(self.movement, -DIFFY)
            if(newy < playablerect.top): self.accuratey = playablerect.top
            elif(newy > playablerect.bottom - self.rect.height): self.accuratey = playablerect.bottom - self.rect.height
            else: self.accuratey = newy
        elif(DIFFY == 0):
            newx = self.accuratex + math.copysign(self.movement, -DIFFX)
            if(newx < playablerect.left): self.accuratex = playablerect.left
            elif(newx > playablerect.right - self.rect.width): self.accuratex = playablerect.right - self.rect.width
            else: self.accuratex = newx
        else:
            newy = self.accuratey + math.copysign(self.movement, -DIFFY)
            if(newy < playablerect.top): self.accuratey = playablerect.top
            elif(newy > playablerect.bottom - self.rect.height): self.accuratey = playablerect.bottom - self.rect.height
            else: self.accuratey = newy
            
            newx = self.accuratex + math.copysign(self.movement, -DIFFX)
            if(newx < playablerect.left): self.accuratex = playablerect.left
            elif(newx > playablerect.right - self.rect.width): self.accuratex = playablerect.right - self.rect.width
            else: self.accuratex = newx
    else:
        while(self.targetx == -1 or self.targety == -1 or (self.targetx == self.rect.x and self.targety == self.rect.y)):
            self.targetx = random.randint(playablerect.left, playablerect.right)
            self.targety = random.randint(playablerect.top, playablerect.bottom)
        DIFFX = self.targetx - self.rect.x
        DIFFY = self.targety - self.rect.y
        DISTANCE = math.sqrt((DIFFX**2)+(DIFFY**2))
        self.accuratex += self.movement * (DIFFX/DISTANCE)
        self.accuratey += self.movement * (DIFFY/DISTANCE)
        
    # Actually move the sprite. We truncate the more accurate versions of their coordinates
    self.rect.x = int(self.accuratex)
    self.rect.y = int(self.accuratey)

    # Super enemies spawn other enemies when fully inside the screen
    if(playablerect.contains(self.rect) and game.gametick - self.lastenemyspawn > game.enemyspawnrate * 2):
        self.lastenemyspawn = game.gametick
        game.enemy_sprites.add(Enemy(game.enemytypes['Tiny Enemy'], self.rect))


class EnemyType:
    def __init__(self, name="Normal", movement=2, spawnrate=1500, image='data/images/enemy-small.png', initfunc=False, updatefunc=DefaultEnemyUpdate):
        self.name = name
        self.movement = movement
        self.spawnrate = spawnrate
        self.lastspawn = 0
        self.image = pygame.image.load(image)
        self.initfunc = initfunc
        self.updatefunc = updatefunc
