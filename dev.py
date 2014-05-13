#!/usr/bin/env python
# Core stuff
import os, sys, random, math
# Pygame
import pygame
from pygame import *

if not pygame.font:
    print 'Warning, fonts disabled'
    sys.exit(1)
if not pygame.mixer:
    print 'Warning, sound disabled'
    sys.exit(1)
# Our files
from interface import *

# Globals
FPS = 60
WIDTH = 640
HEIGHT = 480
STATE_MAINMENU  = 0
STATE_PLAYING   = 1
STATE_GAMEOVER  = 2
STATE_HELP      = 3


class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        # Screen
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        # Fonts
        self.headerfont = pygame.font.Font(None, 36)
        self.gamestatfont = pygame.font.Font(None, 20)
        self.helpfont = pygame.font.Font(None, 24)

        # Inteface
        self.interface = Interface(self.screen)
        self.bottomhudheight = 45
        
        # Start main menu
        self.ChangeState(STATE_MAINMENU)

    def Loop(self):
        pygame.key.set_repeat(500, 30)
        clock = pygame.time.Clock()  
        running = True
        while running:
            # Time
            clock.tick(FPS)
            curtime = self.gametick()
            mousepos = pygame.mouse.get_pos()
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if(self.GetState() == STATE_MAINMENU):
                        # Have they clicked on the start button
                        if(self.startbutton.MouseOver(mousepos)):
                            # Change the game state to playing and update our curtime
                            curtime = self.ChangeState(STATE_PLAYING)
                        if(self.helpbutton.MouseOver(mousepos)):
                            curtime = self.ChangeState(STATE_HELP)
                        # Have they clicked on the quit button
                        elif(self.quitbutton.MouseOver(mousepos)):
                            # Stop the loop
                            running = False
                    elif(self.GetState() == STATE_HELP):
                        if self.returnbutton.MouseOver(mousepos):
                            curtime = self.ChangeState(STATE_MAINMENU)
                    elif(self.GetState() == STATE_PLAYING and (curtime - self.cage.lastrage) > self.cage.ragedelay):
                        # Shooting mechanism
                        self.rage_sprites.add(Rage(self.cage, 0, mousepos))
                        self.cage.lastrage = curtime
                        while(self.cage.rageamount > 1):
                            self.rage_sprites.add(Rage(self.cage, 0, mousepos))
                            self.cage.rageamount -= 1
                        if(mousepos[0] > self.cage.rect.x):
                            self.cage.image = self.cage.rageimg
                        else:
                            self.cage.image = pygame.transform.flip(self.cage.rageimg, True, False)
                    elif(self.GetState() == STATE_GAMEOVER):
                        # Have they clicked on the main menu button
                        if(curtime >= 2000):
                            if self.menubutton.MouseOver(mousepos):
                                # Change the game state to the main menu and update our curtime
                                curtime = self.ChangeState(STATE_MAINMENU)
                            elif self.retrybutton.MouseOver(mousepos):
                                # Change the game state to playing again and update curtime
                                curtime = self.ChangeState(STATE_PLAYING)

            if(self.GetState() == STATE_PLAYING):
                playablearea = self.GetPlayableRect()

                
                # De-Rage Cage
                if((curtime - self.cage.lastrage) > 1000):
                    self.cage.image = self.cage.cageimg
                
                # Enemy Creation
                if((curtime - self.lastenemyspawn) > self.enemyspawnrate):
                    self.lastenemyspawn = curtime
                    self.enemy_sprites.add(Enemy(playablearea))

                # Super Enemy Creation
                if((curtime - self.lastsuperenemyspawn) > 15000):
                    self.lastsuperenemyspawn = curtime
                    self.superenemy_sprites.add(SuperEnemy(playablearea))
                    self.supernumber += 1

                # Super Enemy Changes
                if(self.supernumber >= 1):
                    self.enemyspawnrate = 750
                else:
                    self.enemyspawnrate = 1500

                # Powerup Creation
                if((curtime - self.lastpoweruptime) > 10000):
                    self.lastpoweruptime = curtime
                    self.powerup_sprites.add(PowerUp(self, self.cage, playablearea))

                # Movement stuff
                self.cage.move(key.get_pressed(), playablearea)
                self.enemy_sprites.update(self.cage)
                self.rage_sprites.update(self.rage_sprites, playablearea)
                self.superenemy_sprites.update(self.cage)

                # Collision detection
                # Enemy collides with cage
                collidelist = pygame.sprite.spritecollide(self.cage,self.enemy_sprites,False)
                if collidelist:
                    self.ChangeState(STATE_GAMEOVER)
                    curtime = self.gametick()
                # Enemy collides with bullet
                collidelist = pygame.sprite.groupcollide(self.enemy_sprites,self.rage_sprites,True,self.cage.gothroughpowerup)
                if collidelist:
                    self.score += (5*len(collidelist))
                    if self.cage.rageexplode:
                        self.cage.explosionactivate = True
                        for enemy, ragelist in collidelist.items():
                            self.rage_sprites.add(Rage(self.cage, enemy, mousepos))
                        self.cage.rageexplode = False
                        self.cage.gothroughpowerup = False
                        self.cage.explosiondelay = curtime
                                   
                if ((curtime - self.cage.explosiondelay) > 1000 and self.cage.explosionactivate):
                    self.cage.manualpowerend = True
                        
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
                    self.cage.rageexplode = collidelist[0].rageexplode
                    self.cage.currentdescription = self.cage.powerdescription
                elif (curtime >= self.cage.powerupend and self.cage.powerupend != 0 or (self.cage.manualpowerend)):
                    self.manualpowerend = False
                    self.cage.ragedelay = self.cage.defaultdelay
                    self.cage.powerupend = 0
                    self.cage.gothroughpowerup = True
                    self.cage.rageexplode = False
                    self.cage.explosionactivate = False
                    self.cage.poweruptype = 0
                    self.cage.currentdescription = "None"
                # Scoring

                if((curtime - self.lasttimescore) >= 1000):
                    self.lasttimescore = curtime
                    self.score+=1


                # Chapter Changes

                if((curtime - self.lastchapterchange) >= 30000):
                    self.lastchapterchange = curtime
                    # If the film array is empty (played all the chapters)
                    if(not self.filmarray):
                        self.gameWon = True
                        curtime = self.ChangeState(STATE_GAMEOVER)
                    else:
                        self.ChangeChapter()
            
            # Render stuff

            if self.GetState() == STATE_MAINMENU:
                self.ClearScreen()
                # Title
                text = self.headerfont.render("Nick Cage Film Battle Royale", 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.width/2, centery=self.height/8)
                self.screen.blit(text, textpos)

                # Start button
                if(self.startbutton.MouseOver(mousepos)):
                    self.startbutton.bgcol = (150,0,0)
                else:
                    self.startbutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.startbutton)
                if(self.helpbutton.MouseOver(mousepos)):
                    self.helpbutton.bgcol = (150,0,0)
                else:
                    self.helpbutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.helpbutton)
                if(self.quitbutton.MouseOver(mousepos)):
                    self.quitbutton.bgcol = (150,0,0)
                else:
                    self.quitbutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.quitbutton)
            elif self.GetState() == STATE_HELP:
                self.ClearScreen()

                text = self.headerfont.render("How to Play", 1, (255,0,0))
                textpos = text.get_rect(centerx = self.width/2, centery = self.height/16)
                self.screen.blit(text,textpos)

                text = self.helpfont.render("You are Cage, and you have released a new film", 1, (255,0,0))
                textpos = text.get_rect(centerx = self.width/3, centery = self.height/6)
                self.screen.blit(text,textpos)

                self.helpimage = pygame.image.load('data/images/cage.png')
                self.screen.blit(self.helpimage,(self.width/1.5,self.height/7.5))
                

                text = self.helpfont.render ("Cage refuses to listen to any bad reviews, and must use his Rage to", 1, (255,0,0))
                textpos = text.get_rect(centerx = self.width/2, centery = self.height/3.5)
                self.screen.blit(text,textpos)

                text = self.helpfont.render ("destroy the bad reviews before they can use their Logic against him.", 1, (255,0,0))
                textpos = text.get_rect(centerx = self.width/2, centery = self.height/3)
                self.screen.blit(text,textpos)

                self.helpimage = pygame.image.load ('data/images/cageangry-small.png')
                self.screen.blit(self.helpimage,(self.width/3.5, self.height/2.5))

                self.helpimage = pygame.image.load ('data/images/enemy.png')
                self.screen.blit(self.helpimage,(self.width/1.5, self.height/2.5))
                
                if(self.quitbutton.MouseOver(mousepos)):
                    self.returnbutton.bgcol = (150,0,0)
                else:
                    self.returnbutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.returnbutton)
                
                
            elif self.GetState() == STATE_PLAYING:
                self.ClearScreen()

                self.screen.blit(self.filmbg,(0,0))
                # Sprites
                self.enemy_sprites.draw(self.screen)
                self.superenemy_sprites.draw(self.screen)
                self.cage_sprite.draw(self.screen)
                self.rage_sprites.draw(self.screen)
                self.powerup_sprites.draw(self.screen)
                # Render the text (score, month, film) and the charge meter
                self.RenderPlayingInterface()
                # Starting message
                if (curtime <= 2000):
                    text = self.headerfont.render("Here come the reviews!", 1, (255,0,0))
                    textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                    self.screen.blit(text,textpos)
            elif self.GetState() == STATE_GAMEOVER:
                if (self.gameWon):
                    text = self.headerfont.render("THE RAGE SAVED THE CAGE! WELL DONE!", 1, (255,255,0))
                    textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                    self.screen.blit(text,textpos)
                else:
                    text = self.headerfont.render("THE RAGE COULD NOT SAVE THE CAGE!", 1, (255,255,0))
                    textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
                    self.screen.blit(text,textpos)
                text = self.headerfont.render("Game Over.", 1, (255,255,0))
                textpos = text.get_rect(centerx=self.width/2,centery=(self.height/2+36))
                self.screen.blit(text,textpos)

                # Button
                if(self.menubutton.MouseOver(mousepos)):
                    self.menubutton.bgcol = (150,0,0)
                else:
                    self.menubutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.menubutton)
                if(self.retrybutton.MouseOver(mousepos)):
                    self.retrybutton.bgcol = (150,0,0)
                else:
                    self.retrybutton.bgcol = (255,0,0)
                self.interface.RenderButton(self.retrybutton)
                
            pygame.display.flip()
        pygame.quit()

    def LoadSprites(self):
        self.cage = Cage(self.GetPlayableRect())
        self.cage_sprite = pygame.sprite.RenderPlain((self.cage))
        self.superenemy_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.rage_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()

    # Returns the time since the start of the current state
    def gametick(self):
        return pygame.time.get_ticks() - self.statestarttime

    # Resets the game tick to start from 0 again (used when changing states)
    def gametickstart(self):
        self.statestarttime = pygame.time.get_ticks()

    # Returns the current game state
    def GetState(self):
        return self.gamestate

    # Returns a rect containing the playable area of the screen
    def GetPlayableRect(self):
        return Rect(0, 0, self.width, self.height-self.bottomhudheight)

    """
        ChangeState
        Input: The integer state to change to
        Description: Sets the current game state to input and runs necessary init code
        Returns: The current tick. If state change is successful, this will be 0.
    """
    def ChangeState(self, newstate):
        if newstate == STATE_MAINMENU:
            self.startbutton = Button(Rect(self.width/2 - 100, self.height/2 - 30, 200, 60), "Start")
            self.helpbutton = Button(Rect(self.width/2 - 100, self.startbutton.rect.bottom + self.interface.buttonpadding, 200, 60), "How to Play")
            self.quitbutton = Button(Rect(self.width/2 - 100, self.helpbutton.rect.bottom + self.interface.buttonpadding, 200, 60), "Quit")
        elif newstate == STATE_PLAYING:
            self.LoadSprites()
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

            # Chapters
            self.filmarray = ["National Treasure", "National Treasure 2", "Ghost Rider", "Ghost Rider 2", "Wicker Man", "Bangkok Dangerous", "Vampire's Kiss", "Season of the Witch", "Face/Off", "Sorcerer's Apprectice", "Gone in Sixty Seconds", "Con Air"]
            self.filmbgarray = ["data/films/nationaltreasure.png","data/films/National Treasure 2.jpg", "data/films/Ghost Rider.jpg", "data/films/Ghost Rider 2.jpeg", "data/films/wicker man background.jpg", "data/films/bangkok dangerous background.jpg", "data/films/vampire's kiss background.jpg","data/films/Season of the Witch.jpg","data/films/face off.jpg","data/films/sorcerer's apprentice background.jpg","data/films/Gone in 60 Seconds.jpg","data/films/Con Air.png"]
            self.lastchapterchange = 0
            self.month = 0
            self.ChangeChapter()
        elif newstate == STATE_GAMEOVER:
            self.menubutton = Button(Rect(self.width/2 - 100, self.height/4 - 30, 200, 60), "Main Menu")
            self.retrybutton = Button(Rect(self.width/2 - 100, self.menubutton.rect.bottom + self.interface.buttonpadding, 200, 60), "Retry")
        elif newstate == STATE_HELP:
            self.returnbutton = Button(Rect(self.width/2 - 100, self.height - 125, 200, 60), "Return to Menu")
        else:
            return self.gametick()

        # Now that we've initialized the state, we can update the game's state variable and reset the game tick
        self.gamestate = newstate
        self.gametickstart()
        return self.gametick()
    def ClearScreen(self):
        self.screen.blit(self.background, (0, 0))
    def RenderPlayingInterface(self):
        # "Rage" charge meter
        ragerect = Rect(self.width - 105, self.height - 35, min((float(self.gametick()-self.cage.lastrage)/self.cage.ragedelay) * 100, 100), 30)

        # Interface background
        interfaceborder = Rect(0, self.height - (ragerect.height + 15), self.width, ragerect.height + 15)
        interfacebackground = Rect(0, self.height - (ragerect.height + 10), self.width, ragerect.height + 10)
        
        # Text
        # Score
        score = self.gamestatfont.render("Score: {:d}".format(self.score), 1, (255,0,0))
        scorepos = score.get_rect(left=5,top=5)
        # Month
        month = self.gamestatfont.render ("Month: " + str(self.month), 1, (255,0,0))
        monthpos = month.get_rect(left=5, centery=interfacebackground.centery)
        # Film
        film = self.gamestatfont.render (self.filmtitle, 1, (255,0,0))
        filmpos = film.get_rect(left=monthpos.right + 35, centery=interfacebackground.centery)

        # Powerup
        powerup = self.gamestatfont.render ("Current Powerup: " + self.cage.currentdescription, 1, (255,0,0))
        poweruppos = powerup.get_rect(left = filmpos.right + 35, centery = interfacebackground.centery)

        # Render interface
        pygame.draw.rect(self.screen, (255,0,0), interfaceborder)
        pygame.draw.rect(self.screen, (0,0,0), interfacebackground)
        self.screen.blit(score, scorepos)
        self.screen.blit(month, monthpos)
        self.screen.blit(film, filmpos)
        self.screen.blit(powerup, poweruppos)
        pygame.draw.rect(self.screen, (0,255,0), ragerect)
    def ChangeChapter(self):
        self.curchapter = random.randint(0, (self.filmarray.__len__() - 1))
        self.filmtitle = self.filmarray[self.curchapter]
        self.filmbg = pygame.image.load(self.filmbgarray[self.curchapter])
        del self.filmarray[self.curchapter]
        del self.filmbgarray[self.curchapter]
        self.month += 1
# Cage (player) class
class Cage(pygame.sprite.Sprite):
    def __init__(self, playablerect):
        # Create the cage
        pygame.sprite.Sprite.__init__(self)
        self.cageimg = pygame.image.load('data/images/cage.png')
        self.rageimg = pygame.image.load('data/images/cageangry-small.png')
        self.image = self.cageimg
        self.rect = self.image.get_rect()
        self.powerupgot = 0
        self.powerupend = 0

        # Spawn in center
        self.rect.x = playablerect.right/2 - self.rect.width/2
        self.rect.y = playablerect.bottom/2 - self.rect.height/2

        # Movement
        self.movement = 3
        self.dmovement = self.movement/math.sqrt(2)

        # Attack
        self.lastrage = 0
        self.ragedelay = 2000
        self.rageamount = 1
        self.defaultdelay = self.ragedelay
        self.gothroughpowerup = True
        self.rageexplode = False
        self.explosiondelay = 0
        self.explosionactivate = False
        self.manualpowerend = False
        self.poweruptype = 0

        # PowerUp Descriptions
        self.powerdescription = "None"
        self.currentdescription = "None"
        
    def move(self, keys_pressed, playablerect):
        # Used to track how much we should move in x and y
        xmove = 0
        ymove = 0
        
        # Previously pressed keys still held down
        if(keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]):
            if(self.rect.right + self.movement <= playablerect.right):
               xmove += self.movement
        if(keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]):
            if(self.rect.left - self.movement >= playablerect.left):
                xmove = -self.movement
        if(keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]):
            if(self.rect.top - self.movement >= playablerect.top):
                ymove = -self.movement
        if(keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]):
            if(self.rect.bottom + self.movement <= playablerect.bottom):
               ymove += self.movement
        #If the player is trying to move in x and y, move diagonally
        if(xmove and ymove):
            xmove = math.copysign(self.dmovement, xmove)
            ymove = math.copysign(self.dmovement, ymove)
        self.rect.x += xmove
        self.rect.y += ymove

class Rage(pygame.sprite.Sprite):
    def __init__(self, cage, enemy, mousepos):
        # Create rage
        pygame.sprite.Sprite.__init__(self)
        if(cage.rageamount == 1):
            if(cage.poweruptype == 0):
                self.base_image = pygame.image.load('data/images/rage-small.png')
            
            elif(cage.poweruptype == 1):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 2):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 3):
                self.base_image = pygame.image.load('data/images/rage-small.png')
            
            elif(cage.poweruptype == 4):
                self.base_image = pygame.image.load('data/images/ghostriderskull.png')
                
            elif(cage.poweruptype == 5):
                self.base_image = pygame.image.load('data/images/bee.png')
                cage.rageamount = 10 
                
            elif(cage.poweruptype == 6):
                self.base_image = pygame.image.load('data/images/bangkokrage.png')
                
            elif(cage.poweruptype == 7):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 8):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 9):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
                cage.rageamount = 6
                
            elif(cage.poweruptype == 10 and cage.explosionactivate):
                self.base_image = pygame.image.load('data/images/explosion.png')

            elif(cage.poweruptype == 10 and not cage.explosionactivate):
                self.base_image = pygame.image.load('data/images/magicorb.png')
                
            elif(cage.poweruptype == 11):
                self.base_image = pygame.image.load('data/images/rage-small.png')
                
            elif(cage.poweruptype == 12):
                self.base_image = pygame.image.load('data/images/rage-small.png')
        else:
            if(cage.poweruptype == 9):
                self.base_image = pygame.image.load('data/images/rage-tiny.png')
            if(cage.poweruptype == 5):
                self.base_image = pygame.image.load('data/images/bee.png')
            
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Spawn where cage is
        self.rect.x = (cage.rect.x + cage.rect.width/2)
        self.rect.y = (cage.rect.y + cage.rect.height/2)

        if(cage.poweruptype == 10 and cage.explosionactivate):
            self.rect.x = (enemy.rect.x + enemy.rect.width/2)
            self.rect.y = (enemy.rect.y + enemy.rect.height/2)

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

        if(cage.poweruptype == 9 or cage.poweruptype == 5):
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

        if(cage.poweruptype == 10 and cage.explosionactivate):
            self.movex = 0
            self.movey = 0
        
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
        if(cage.poweruptype == 9):
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

        
    def update(self, spritegroup, playablerect):
        self.accuratex -= self.movex
        self.accuratey -= self.movey
        self.rect.x = int(self.accuratex - self.rect.width/2)
        self.rect.y = int(self.accuratey - self.rect.height/2)

        if((self.rect.left > playablerect.right)
           or(self.rect.top > playablerect.bottom)
           or(self.rect.right < playablerect.left)
           or(self.rect.bottom < playablerect.top)):
            spritegroup.remove(self)

class PowerUp(pygame.sprite.Sprite):

    def __init__(self, main, cage, playablerect):
        pygame.sprite.Sprite.__init__(self)
        uniquepower = random.randint(1,3)
        self.gothroughpowerup = True
        self.rageexplode = False
        self.ragedelay = 2000
        self.length = 5000
        if(uniquepower == 3):
            if(main.filmtitle == "National Treasure"):
                self.image = pygame.image.load('data/images/national1powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 1
                cage.powerdescription = "Declaration of Independence"
            elif(main.filmtitle == "National Treasure 2"):
                self.image = pygame.image.load('data/images/national2powerup.png')
                self.ragedelay = 500
                self.poweruptype = 2
                cage.powerdescription = "Illuminati Coin"
            elif(main.filmtitle == "Ghost Rider"):
                self.image = pygame.image.load('data/images/ghostriderchain.png')
                self.gothroughpowerup = False
                self.ragedelay = 1500
                self.poweruptype = 3
                cage.powerdescription = "Ghost Rider Chain"
            elif(main.filmtitle == "Ghost Rider 2"):
                self.image = pygame.image.load('data/images/ghostriderskull.png')
                self.gothroughpowerup = False
                self.ragedelay = 1500
                self.poweruptype = 4
                cage.powerdescription = "Ghost Rider Skull"
            elif(main.filmtitle == "Wicker Man"):
                self.image = pygame.image.load('data/images/bee.png')
                self.ragedelay = 1000
                self.poweruptype = 5
                cage.powerdescription = "BEES"
            elif(main.filmtitle == "Bangkok Dangerous"):
                self.image = pygame.image.load('data/images/bangkokpowerup.png')
                self.ragedelay = 300
                self.poweruptype = 6
                cage.powerdescription = "Uzi"
            elif(main.filmtitle == "Vampire's Kiss"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 7
                cage.powerdescription = "Vampire Teeth"
            elif(main.filmtitle == "Season of the Witch"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 8
                cage.powerdescription = "Witch Sword"
            elif(main.filmtitle == "Face/Off"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1500
                self.poweruptype = 9
                cage.powerdescription = "Travolta's Face"
            elif(main.filmtitle == "Sorcerer's Apprectice"):
                self.image = pygame.image.load('data/images/magicorb.png')
                self.rageexplode = True
                self.ragedelay = 2500
                self.length = 500000
                self.poweruptype = 10
                cage.powerdescription = "Explosive Orb"
            elif(main.filmtitle == "Con Air"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 11
                cage.powerdescription = "Cage's Long Hair"
            elif(main.filmtitle == "Gone in Sixty Seconds"):
                self.image = pygame.image.load('data/images/powerup.png')
                self.ragedelay = 1000
                self.poweruptype = 12
                cage.powerdescription = "Mustang"
        else:
            self.image = pygame.image.load('data/images/powerup.png')
            self.ragedelay = 1000
            self.gothroughpowerup = True
            self.poweruptype = 0
            cage.powerdescription = "Good Review"

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(playablerect.left, playablerect.right-self.rect.width)
        self.rect.y = random.randint(playablerect.top, playablerect.bottom-self.rect.height)

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, playablerect):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image('enemy-small.png',255)
        self.image = pygame.image.load('data/images/enemy-small.png')
        self.rect = self.image.get_rect()
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
        self.rect.x = startX
        self.rect.y = startY
        self.accuratex = startX
        self.accuratey = startY
        self.movement = 2
        
    def update(self, cage):
        # Work out the difference in position between the enemy and the player
        DIFFX = cage.rect.x - self.rect.x
        DIFFY = cage.rect.y - self.rect.y
        DISTANCE = math.sqrt((DIFFY**2)+(DIFFX**2))
        if(DISTANCE < self.movement):
            self.accuratex = cage.rect.x
            self.accuratey = cage.rect.y
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

class SuperEnemy(pygame.sprite.Sprite):
    def __init__(self, playablerect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/images/youtube-logo.png')
        self.rect = self.image.get_rect()
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
