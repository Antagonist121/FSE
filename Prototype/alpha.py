#!/usr/bin/env python
import os, sys, random, math
import pygame
from pygame import *


if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Globals
WIDTH = 640
HEIGHT = 480

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Scoring
        self.score = 0
        self.lasttimescore = 0

    def Loop(self):
        self.LoadSprites()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        pygame.key.set_repeat(500, 30)
        clock = pygame.time.Clock()

        lastenemyspawn = 0
        
        running = True
        while running:
            # Time
            clock.tick(60)
            curtime = pygame.time.get_ticks()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if((curtime - self.cage.lastrage) > 2000):
                        self.rage_sprites.add(Rage(self.cage, pygame.mouse.get_pos()))
                        self.cage.lastrage = curtime
                        self.cage.image = self.cage.rageimg

            # De-Rage Cage
            if((curtime - self.cage.lastrage) > 1000):
                self.cage.image = self.cage.cageimg
            
            # Enemy Creation
            if((curtime - lastenemyspawn) > 2000):
                lastenemyspawn = curtime
                self.enemy_sprites.add(Enemy())

            # Movement stuff
            self.cage.move(key.get_pressed())
            self.enemy_sprites.update(self.cage)
            self.rage_sprites.update(self.rage_sprites)

            # Collision detection
            # Enemy collides with cage
            collidelist = pygame.sprite.spritecollide(self.cage,self.enemy_sprites,False)
            if collidelist:
                if pygame.font:
                    running = False
            # Enemy collides with bullet
            collidelist = pygame.sprite.groupcollide(self.enemy_sprites,self.rage_sprites,True,True)

            # Scoring
            self.score += (5*len(collidelist))
            if(len(collidelist) > 0):
                print(self.score)
            if((curtime - self.lasttimescore) >= 1000):
                self.lasttimescore = curtime
                self.score+=1

            
            # Render stuff
            self.screen.blit(self.background, (0, 0))
            # Text
            if pygame.font:
                font = pygame.font.Font(None,36)
                text = font.render("Score: {:d}".format(self.score), 1, (255,0,0))
                textpos = text.get_rect(centerx=self.width/2)
                self.screen.blit(text,textpos)
                if not running:
                        font = pygame.font.Font(None,36)
                        text = font.render("THE RAGE COULD NOT SAVE THE CAGE!", 1, (255,255,0))
                        textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                        self.screen.blit(text,textpos)
                        text = font.render("Game Over.", 1, (255,255,0))
                        textpos = text.get_rect(centerx=self.width/2,centery=(self.height/2+36))
                        self.screen.blit(text,textpos)
            # Sprites
            self.enemy_sprites.draw(self.screen)
            self.cage_sprite.draw(self.screen)
            self.rage_sprites.draw(self.screen)
            pygame.display.flip()
        pygame.time.delay(10000)
        pygame.quit()

    def LoadSprites(self):
        self.cage = Cage()
        self.cage_sprite = pygame.sprite.RenderPlain((self.cage))
        self.enemy_sprites = pygame.sprite.Group()
        self.rage_sprites = pygame.sprite.Group()

class Cage(pygame.sprite.Sprite):
    def __init__(self):
        # Create the cage
        pygame.sprite.Sprite.__init__(self)
        self.cageimg = pygame.image.load('data/images/cage.png')
        self.rageimg = pygame.image.load('data/images/cageangry-small.png')
        self.image = self.cageimg
        self.rect = self.image.get_rect()

        # Spawn in center
        self.rect.x = WIDTH/2 - self.rect.width/2
        self.rect.y = HEIGHT/2 - self.rect.height/2

        # Movement
        self.movement = 3
        self.dmovement = self.movement/math.sqrt(2)

        # Attack
        self.lastrage = 0
        self.ragedelay = 2000

    def move(self,keys_pressed):
        # Used to track how much we should move in x and y
        xmove = 0
        ymove = 0
        
        # Previously pressed keys still held down
        if(keys_pressed[pygame.K_RIGHT]):
            if(self.rect.x + self.movement + self.rect.width <= WIDTH):
               xmove += self.movement
        if(keys_pressed[pygame.K_LEFT]):
            if(self.rect.x - self.movement >= 0):
                xmove = -self.movement
        if(keys_pressed[pygame.K_UP]):
            if(self.rect.y - self.movement >= 0):
                ymove = -self.movement
        if(keys_pressed[pygame.K_DOWN]):
            if(self.rect.y + self.movement + self.rect.height <= HEIGHT):
               ymove += self.movement
        if(xmove and ymove):
            xmove = math.copysign(self.dmovement, xmove)
            ymove = math.copysign(self.dmovement, ymove)
        self.rect.x += xmove
        self.rect.y += ymove

class Rage(pygame.sprite.Sprite):
    def __init__(self,cage,mousepos):
        # Create rage
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/images/rage-small.png')
        self.rect = self.image.get_rect()

        # Spawn where cage is
        self.rect.x = cage.rect.x
        self.rect.y = cage.rect.y

        # Movement
        self.movement = 5
        DIFFX = cage.rect.x - mousepos[0]
        DIFFY = cage.rect.y - mousepos[1]
        DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
        self.movex = int(self.movement * (DIFFX / DISTANCE)) + math.copysign(1,DIFFX)
        self.movey = int(self.movement * (DIFFY / DISTANCE)) + math.copysign(1,DIFFY)

    def update(self,spritegroup):
        self.rect.x -= self.movex
        self.rect.y -= self.movey

        if((self.rect.x > WIDTH)
           or(self.rect.y > HEIGHT)
           or(self.rect.x + self.rect.width < 0)
           or(self.rect.y + self.rect.height <0)):
            spritegroup.remove(self)
            print("Rage deleted")

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image('enemy-small.png',255)
        self.image = pygame.image.load('data/images/enemy-small.png')
        self.rect = self.image.get_rect()
        startLine = random.randint(0,3)
        if(startLine == 0):
            startY = -self.rect.height
            startX = random.randint(0,WIDTH)
        if(startLine == 2):
            startY = HEIGHT
            startX = random.randint(0,WIDTH)
        if(startLine == 1):
            startX = WIDTH
            startY = random.randint(0,HEIGHT)
        if(startLine == 3):
            startX = -self.rect.width
            startY = random.randint(0,HEIGHT)
        self.rect.x = startX
        self.rect.y = startY
        self.movement = 2
        
    def update(self, cage):
        DIFFX = cage.rect.x - self.rect.x
        DIFFY = cage.rect.y - self.rect.y
        DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
        if(DISTANCE < self.movement):
            self.rect.x = cage.rect.x
            self.rect.y = cage.rect.y
        elif(DIFFX == 0):
            self.rect.y += math.copysign(self.movement, DIFFY)
        elif(DIFFY == 0):
            self.rect.x += math.copysign(self.movement, DIFFX)
        else:
            changex = int(self.movement * (DIFFX/DISTANCE))
            changey = int(self.movement * (DIFFY/DISTANCE))
            if(changex == 0):
                changey += math.copysign(1, DIFFY)
            if(changey == 0):
                changex += math.copysign(1, DIFFX)
            changedist = math.sqrt((changex**2)+(changey**2))
            self.rect.x += changex
            self.rect.y += changey


        
if __name__ == "__main__":
    window = Game()
    window.Loop()
