class PowerUp(pygame.sprite.Sprite):

    def __init__(self, main):

        uniquepower = random.randint(1,3)
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
