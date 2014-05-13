# Pygame
import pygame
from pygame import *

if not pygame.font:
    print 'Warning, fonts disabled'
    sys.exit(1)

# Interface class
class Interface:
    def __init__(self, screen):
        self.buttonfont = pygame.font.Font(None, 36)
        self.textboxfont = pygame.font.Font(None, 26)
        self.screen = screen
        self.buttonpadding = 10 # Gap between buttons
        self.padding = 5 # General padding around elements
        
    def RenderButton(self, button):
        pygame.draw.rect(self.screen, button.bgcol, button.rect)
        text = self.buttonfont.render(button.message, 1, (0,0,0))
        textpos = text.get_rect(centerx=button.rect.left+(button.rect.width/2),centery=button.rect.top+(button.rect.height/2))
        self.screen.blit(text,textpos)
        
    def RenderTextbox(self, textbox):
        text = self.textboxfont.render(textbox.message, 1, textbox.textcol)
        textpos = text.get_rect(centerx=textbox.pos[0],centery=textbox.pos[1])
        
        boxsize = [textpos.width + self.padding * 4, textpos.height + self.padding * 4]
        borderrect = Rect(textbox.pos[0]-boxsize[0]/2, textbox.pos[1]-boxsize[1]/2, boxsize[0], boxsize[1])
        
        boxsize[0] -= self.padding * 2
        boxsize[1] -= self.padding * 2
        backgroundrect = Rect(textbox.pos[0]-boxsize[0]/2, textbox.pos[1]-boxsize[1]/2, boxsize[0], boxsize[1])

        pygame.draw.rect(self.screen, textbox.bordercol, borderrect)
        pygame.draw.rect(self.screen, textbox.bgcol, backgroundrect)
        self.screen.blit(text, textpos)

# Button class- requires a rectangle for the button and a message
class Button:
    def __init__(self, rect, message):
        self.rect = rect
        self.message = message
        self.bgcol = (255,0,0)
    def MouseOver(self, mousepos):
        if(mousepos[0] < self.rect.left or mousepos[0] > self.rect.right):return False
        if(mousepos[1] < self.rect.top or mousepos[1] > self.rect.bottom):return False
        return True

# Textbox class- requires a position for the center and a message. Doesn't support new lines
class Textbox:
    def __init__(self, pos, message):
        self.pos = pos
        self.message = message
        self.bgcol = (0,0,0)
        self.bordercol = (255,0,0)
        self.textcol = (255,255,255)
