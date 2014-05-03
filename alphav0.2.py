#!/usr/bin/env python
import os, sys, random, math
import pygame
from pygame import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#Global Variables
WIDTH = 640
HEIGHT = 480

class Game:
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Scoring
        self.score = 0
        self.lasttimescore = 0

        # Spawning
        self.lastpowerupspawn = 0
        self.lastenemyspawn = 0

    def Loop(self):
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.LoadSprites()

        pygame.key.set_repeat(500, 30)
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(60)
            curtime = pygame.time.get_ticks()
            # IMPORTANT DO NOT CALL pygame.event.get() MORE THAN ONCE AT A TIME
           # for event in pygame.event.get():
            # #   if event.type == pygame.QUIT:
            #        running = False
           #     elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #        print "Click"
            
            self.cage.update(curtime)
            pygame.display.flip()
            
        pygame.quit()

    def LoadSprites(self):
        self.cage = Cage()
        self.cage_sprite = pygame.sprite.RenderPlain((self.cage))
        #self.enemy_sprites = pygame.sprite.Group()
        #self.rage_sprites = pygame.sprite.Group()
        #self.powerup_sprites = pygame.sprite.Group()

    #def LoadScreens(self):
        #self.mainmenu = Screen()
        #self.gamescreen = Screen()
        #self.gameover = Screen()
        #self.mainmenu.AddButton(Button())

class Cage(pygame.sprite.Sprite):
    def __init__(self):
        # Create the cage
        pygame.sprite.Sprite.__init__(self)
        self.cageimg = pygame.image.load('data/images/cage.png')
        self.rageimg = pygame.image.load('data/images/cageangry-small.png')
        self.image = self.cageimg
        self.rect = self.image.get_rect()
        self.powerupgot = 0
        self.powerupend = 0

        # Spawn in center
        self.rect.x = WIDTH/2 - self.rect.width/2
        self.rect.y = HEIGHT/2 - self.rect.height/2

        # Movement
        self.speed = 3

        # Works out change in x and y for diagonal movement
        self.diagonalspeed = float(self.speed)/math.sqrt(2) 
        self.accuratex = float(self.rect.x)
        self.accuratey = float(self.rect.y)

        # Attack
        self.lastrage = 0
        self.ragedelay = 2000
        self.defaultdelay = self.ragedelay


    def Move(self,keys_pressed):
        xmove = 0
        ymove = 0

        if(keys_pressed[pygame.K_RIGHT]):
            if(self.rect.x + self.speed + self.rect.width <= WIDTH):
                xmove += self.speed
        if(keys_pressed[pygame.K_LEFT]):
            if(self.rect.x - self.movement >= 0):
                xmove = -self.speed
        if(keys_pressed[pygame.K_UP]):
            if(self.rect.y - self.movement >= 0):
                ymove = -self.speed
        if(keys_pressed[pygame.K_DOWN]):
            if(self.rect.y + self.speed + self.rect.height <= HEIGHT):
                ymove += self.speed
        if(xmove and ymove):
            xmove = math.copysign(self.diagonalspeed, xmove)
            ymove = math.copysign(self.diagonalspeed, ymove)
        # Storing the accurate movement in float, then truncating to update x & y
        self.accuratex += xmove
        self.accuratey += ymove
        self.rect.x = int(self.accuratex)
        self.rect.y = int(self.accuratey)


    def ChangeSpeed(self,newspeed):
        self.speed = newspeed
        self.diagonalspeed = float(self.speed)/math.sqrt(2)

    def RageCage(self, mousepos, curtime):
        if(mousepos[0] > self.rect.x):
            self.image = self.rageimg
        else:
            self.image = pygame.transform.flip(self.rageimg, True, False)
        self.lastrage = curtime

    def update(self, curtime):
        #if((curtime - self.lastrage) > 1000):
        #    self.image = self.cageimg
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print "Hallo peolpe"
"""
class Rage(pygame.sprite.Sprite):
    def __init__(self,cage,mousepos):
        
    




    def update(self,spritegroup):




class PowerUp(pygame.sprite.Sprite):
    def __init__(self):




    def update(self,spritegroup):

class Enemy(pygame.sprite.Sprite):
    def __init__(self):






    def update(self,cage):


class Screen():
    self.buttons = []
    
    def __init__(self):
        

    def AddButton(self, button):
        self.buttons.append(button)
    






class Button():
    def __init__(self, pos, size, text, onclick):
        self.button = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.textpos = text.get_rect(centerx=pos[0]+size[0], centery=pos[1]+size[1])
        
    def Render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.button)
        self.screen.blit(self.text, self.textpos)

class Chapter():
    def __init__(self,name,poweruparray):
        
        
        
    def GetRandomPowerup(self):

        
class ScreenText():
    def __init__(self,xpos,ypos,fontsize,text):
"""
if __name__ == "__main__":
    window = Game()
    window.Loop()
