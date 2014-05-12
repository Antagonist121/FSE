#!/usr/bin/env python
import os, sys, random, math
import pygame
from pygame import *


if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Globals
WIDTH = 640
HEIGHT = 480
RAGENUMBER = 0

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Scoring
        self.score = 0
        self.lasttimescore = 0
        self.gameWon = False

        # Spawning
        self.lastpoweruptime = 0
        self.lastenemyspawn = 0
        self.lastsuperenemyspawn = 0
        self.supernumber = 0
        self.enemyspawnrate = 1500

        # Theme
        self.film = 0
        self.filmtitle = "National Treasure"
        self.filmarray = ["National Treasure 2", "Ghost Rider", "Ghost Rider 2", "Wicker Man", "Bangkok Dangerous", "Vampire's Kiss", "Season of the Witch", "Face/Off", "Sorcerer's Apprectice", "Gone in Sixty Seconds", "Con Air"]

        # Chapter Number
        self.curchapter = 1
        self.lastchapterchange = 0

        # Interface
        self.rageomfg = Rect(WIDTH - 125,HEIGHT-25,125,25)

    def Loop(self):
        self.LoadSprites()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        font = pygame.font.Font(None,36)
        text = font.render("Nic Cage is releasing a new film!", 1, (255,0,0))
        textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
        self.screen.blit(text,textpos)
        pygame.display.flip()
        pygame.time.delay(2000)
        poster = pygame.image.load("data/images/movie-1.png")
        self.screen.blit(poster,(0,0))
        pygame.display.flip()
        pygame.time.delay(2000)
        initialDelay = 5000
        

        pygame.key.set_repeat(500, 30)
        clock = pygame.time.Clock()
        
        
        running = True
        while running:
            # Time
            clock.tick(60)
            curtime = pygame.time.get_ticks() - initialDelay

            
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if((curtime - self.cage.lastrage) > self.cage.ragedelay):
                        mousepos = pygame.mouse.get_pos()
                        self.rage_sprites.add(Rage(self.cage, mousepos))
                        while(self.cage.rageamount > 1):
                            self.rage_sprites.add(Rage(self.cage, mousepos))
                            self.cage.rageamount -= 1
                        self.cage.lastrage = curtime
                        if(mousepos[0] > self.cage.rect.x):
                            self.cage.image = self.cage.rageimg
                        else:
                            self.cage.image = pygame.transform.flip(self.cage.rageimg, True, False)

            # De-Rage Cage
            if((curtime - self.cage.lastrage) > 1000):
                self.cage.image = self.cage.cageimg
            
            # Enemy Creation
            if((curtime - self.lastenemyspawn) > self.enemyspawnrate):
                self.lastenemyspawn = curtime
                self.enemy_sprites.add(Enemy())

            # Super Enemy Creation
            if((curtime - self.lastsuperenemyspawn) > 15000):
                self.lastsuperenemyspawn = curtime
                self.superenemy_sprites.add(SuperEnemy())
                self.supernumber += 1

            # Super Enemy Changes
            if(self.supernumber >= 1):
                self.enemyspawnrate = 7500
            else:
                self.enemyspawnrate = 15000

            # Powerup Creation
            if((curtime - self.lastpoweruptime) > 1000):
                self.lastpoweruptime = curtime
                self.powerup_sprites.add(PowerUp(self))

            # Movement stuff
            self.cage.move(key.get_pressed())
            self.enemy_sprites.update(self.cage)
            self.rage_sprites.update(self.rage_sprites)
            self.superenemy_sprites.update(self.cage)

            # Collision detection
            # Enemy collides with cage
            collidelist = pygame.sprite.spritecollide(self.cage,self.enemy_sprites,False)
            if collidelist:
                if pygame.font:
                    running = False
            # Enemy collides with bullet
            collidelist = pygame.sprite.groupcollide(self.enemy_sprites,self.rage_sprites,True,self.cage.gothroughpowerup)
            if collidelist:
                    self.score += (5*len(collidelist))
            # Super Enemy collides with bullet
            collidelist = pygame.sprite.groupcollide(self.superenemy_sprites,self.rage_sprites,True,self.cage.gothroughpowerup)
            if collidelist:
                    self.score += (10*len(collidelist))
                    self.supernumber -= 1
            # Cage Collides with powerup
            collidelist = pygame.sprite.spritecollide(self.cage,self.powerup_sprites,True)
            if collidelist:
                self.cage.powerupgot = curtime
                self.cage.powerupend = curtime + collidelist[0].length
                self.cage.ragedelay = collidelist[0].ragedelay
                self.cage.gothroughpowerup = collidelist[0].gothroughpowerup
                self.cage.poweruptype = collidelist[0].poweruptype
            elif (curtime >= self.cage.powerupend and self.cage.powerupend != 0):
                self.cage.ragedelay = self.cage.defaultdelay
                self.cage.powerupend = 0
                self.cage.gothroughpowerup = True
                self.cage.poweruptype = 0
                
            # Scoring

            if((curtime - self.lasttimescore) >= 1000):
                self.lasttimescore = curtime
                self.score+=1


            # Chapter Changes

            if((curtime - self.lastchapterchange) >= 11000):
                self.lastchapterchange = curtime
                if(self.curchapter >= 12):
                    self.gameWon = True
                    running = False
                else:
                    self.curchapter+=1
                    self.filmtitle = self.filmarray[random.randint(0,(self.filmarray.__len__() - 1))]
                    self.filmarray.remove(self.filmtitle)
         
            # Render stuff
            self.screen.blit(self.background, (0, 0))

            

            # Sprites
            self.enemy_sprites.draw(self.screen)
            self.superenemy_sprites.draw(self.screen)
            self.cage_sprite.draw(self.screen)
            self.rage_sprites.draw(self.screen)
            self.powerup_sprites.draw(self.screen)

            if (curtime < 2000):
                text = font.render("Here come the reviews!", 1, (255,0,0))
                textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                self.screen.blit(text,textpos)
                
            # Rage-o-meter
            tempwidth = (float(curtime-self.cage.lastrage)/self.cage.ragedelay) * 125
            if (tempwidth > 125):
                tempwidth = 125
            
            self.rageomfg.width = tempwidth
            
            pygame.draw.rect(self.screen,(255,0,0),self.rageomfg)
            
            # Text
            if pygame.font:
                font = pygame.font.Font(None,36)
                text = font.render("Score: {:d}".format(self.score), 1, (255,0,0))
                textpos = text.get_rect(centerx=self.width/2)
                self.screen.blit(text,textpos)
                text2 = font.render ("Current Film: " + self.filmtitle, 1, (255,0,0))
                textpos = text.get_rect(centerx=self.width/8,centery=(HEIGHT - 20))
                self.screen.blit(text2,textpos)
                text3 = font.render ("Current Month: " + str(self.curchapter), 1, (255,0,0))
                textpos = text.get_rect(centerx=self.width/8, centery = (HEIGHT - 100))
                self.screen.blit(text3,textpos)
                
                if not running:
                    if (self.gameWon):
                        font = pygame.font.Font(None,36)
                        text = font.render("THE RAGE SAVED THE CAGE! WELL DONE!", 1, (255,255,0))
                        textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                        self.screen.blit(text,textpos)
                    else:
                        font = pygame.font.Font(None,36)
                        text = font.render("THE RAGE COULD NOT SAVE THE CAGE!", 1, (255,255,0))
                        textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                        self.screen.blit(text,textpos)
                    text = font.render("Game Over.", 1, (255,255,0))
                    textpos = text.get_rect(centerx=self.width/2,centery=(self.height/2+36))
                    self.screen.blit(text,textpos)
                    
            pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()

    def LoadSprites(self):
        self.cage = Cage()
        self.cage.poweruptype = 0
        self.cage_sprite = pygame.sprite.RenderPlain((self.cage))
        self.superenemy_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.rage_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()

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
        self.movement = 3
        self.dmovement = self.movement/math.sqrt(2)

        # Attack
        self.lastrage = 0
        self.ragedelay = 2000
        self.rageamount = 1
        self.defaultdelay = self.ragedelay
        self.gothroughpowerup = True

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
    def __init__(self,cage, mousepos):
        # Create rage
        pygame.sprite.Sprite.__init__(self)
        if(cage.rageamount == 1):
            cage.rageamount = 1
            if(cage.poweruptype == 0):
                self.base_image = pygame.image.load('data/images/rage-small.png')
            
            elif(cage.poweruptype == 1):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 2):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 3):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
                cage.rageamount = 6
                            
            elif(cage.poweruptype == 4):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 5):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
                cage.rageamount = 10 
                
            elif(cage.poweruptype == 6):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 7):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 8):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 9):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 10):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 11):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 12):
                self.base_image = pygame.image.load('data/images/rage-small.png')
        else:
            if(cage.poweruptype == 3):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
            if(cage.poweruptype == 5):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
                
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Spawn where cage is
        self.rect.x = (cage.rect.x + cage.rect.width/2)
        self.rect.y = (cage.rect.y + cage.rect.height/2)

        # Movement
        self.accuratex = self.rect.x
        self.accuratey = self.rect.y
        self.movement = 5
        DIFFX = self.rect.x - mousepos[0]
        DIFFY = self.rect.y - mousepos[1]
        DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
        if(cage.poweruptype == 5):
            if(cage.rageamount > 1 and cage.rageamount <= 6):
                DIFFX -= ((cage.rageamount - 3) * (DIFFX * 0.25))
                DIFFY -= ((cage.rageamount - 3) * (DIFFY * 0.25))
            if(cage.rageamount > 6 and cage.rageamount <= 10):
                DIFFX += ((cage.rageamount - 7) * (DIFFX * 0.25))
                DIFFY += ((cage.rageamount - 7) * (DIFFY * 0.25))
        self.movex = self.movement * (DIFFX / DISTANCE)
        self.movey = self.movement * (DIFFY / DISTANCE)

        if(cage.poweruptype == 3):
            if(cage.rageamount > 2 and cage.rageamount <= 4):
                if(self.movey < 0 and self.movex < 0):
                    self.movex -= ((cage.rageamount - 1) * 0.3)
                    self.movey += ((cage.rageamount - 1) * 0.5)
                elif(self.movey > 0 and self.movex > 0):
                    self.movex += ((cage.rageamount - 1) * 0.3)
                    self.movey -= ((cage.rageamount - 1) * 0.5)
                else:
                    self.movex += ((cage.rageamount - 1) * 0.3)
                    self.movey += ((cage.rageamount - 1) * 0.5)
            if(cage.rageamount > 4 and cage.rageamount <= 6):
                if(self.movey < 0 or self.movex < 0):
                    self.movex += ((cage.rageamount - 3) * 0.3)
                    self.movey -= ((cage.rageamount - 3) * 0.5)
                elif(self.movey > 0 and self.movex > 0):
                    self.movex -= ((cage.rageamount - 3) * 0.3)
                    self.movey += ((cage.rageamount - 3) * 0.5)
                else:
                    self.movex -= ((cage.rageamount - 3) * 0.3)
                    self.movey -= ((cage.rageamount - 3) * 0.5)

        # Rotation
        if(DIFFY/DISTANCE > 1):
            rotate = math.acos(1)
        elif(DIFFY/DISTANCE < -1):
            rotate = math.acos(-1)
        else:
            rotate = math.acos((DIFFY/DISTANCE))
        rotate = (rotate / math.pi) * 180.0
        if(DIFFX > 0):
            if(DIFFY <= 0):
                rotate = (180 - rotate) + 180
            else:
                rotate = 360 - rotate
        if(cage.poweruptype == 3):
            if(cage.rageamount > 2 and cage.rageamount <= 4):
                if(self.movex > 0 and self.movey < 0):
                    rotate += ((cage.rageamount-3) * 10)
                else:
                    rotate -= ((cage.rageamount-3) * 10)
            if(cage.rageamount > 4 and cage.rageamount <= 6):
                if(self.movex > 0 and self.movey < 0):
                    rotate -= ((cage.rageamount-3) * 10)
                else:
                    rotate += ((cage.rageamount-3) * 10)
        if(cage.poweruptype == 5):
            if(cage.rageamount > 1 and cage.rageamount <= 6):
                rotate -= ((cage.rageamount-1) * 18)
            if(cage.rageamount > 6 and cage.rageamount <= 10):
                rotate += ((cage.rageamount-3) * 18)

        self.image = pygame.transform.rotate(self.image, -rotate)
        
    def update(self,spritegroup):
        self.accuratex -= self.movex
        self.accuratey -= self.movey
        self.rect.x = int(self.accuratex - self.rect.width/2)
        self.rect.y = int(self.accuratey - self.rect.height/2)

        if((self.rect.x > WIDTH)
           or(self.rect.y > HEIGHT)
           or(self.rect.x + self.rect.width < 0)
           or(self.rect.y + self.rect.height <0)):
            spritegroup.remove(self)


class PowerUp(pygame.sprite.Sprite):

    def __init__(self, main):
        pygame.sprite.Sprite.__init__(self)

        uniquepower = random.randint(3,3)
        self.gothroughpowerup = True
        self.ragedelay = 2000
        if(uniquepower == 3):
            if(main.filmtitle == "National Treasure"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 1
            elif(main.filmtitle == "National Treasure 2"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 500
                self.poweruptype = 2
            elif(main.filmtitle == "Ghost Rider"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.gothroughpowerup = False
                self.ragedelay = 2000
                self.poweruptype = 3
            elif(main.filmtitle == "Ghost Rider 2"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.gothroughpowerup = False
                self.ragedelay = 1500
                self.poweruptype = 4
            elif(main.filmtitle == "Wicker Man"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 5
            elif(main.filmtitle == "Bangkok Dangerous"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 6
            elif(main.filmtitle == "Vampire's Kiss"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 7
            elif(main.filmtitle == "Season of the Witch"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 8
            elif(main.filmtitle == "Face/Off"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 9
            elif(main.filmtitle == "Sorcerer's Apprectice"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 10
            elif(main.filmtitle == "Con Air"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 11
            elif(main.filmtitle == "Gone in Sixty Seconds"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 12
        else:
            self.image = pygame.image.load('data/images/powerup.png')
            self.ragedelay = 1000
            self.gothroughpowerup = True
            self.poweruptype = 0
        self.poweruptype = 3
        self.rect = self.image.get_rect()
        self.length = 5000
        self.rect.x = random.randint(0,WIDTH)
        self.rect.y = random.randint(0,HEIGHT)

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

class SuperEnemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/images/youtube-logo.png')
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
        self.movement = 1

    def update(self,cage):
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