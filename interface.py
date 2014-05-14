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
        self.bordersize = 3 # Size of borders in pixels
        
    def RenderButton(self, button):
        pygame.draw.rect(self.screen, button.bgcol, button.rect)
        text = self.buttonfont.render(button.message, 1, (0,0,0))
        textpos = text.get_rect(centerx=button.rect.left+(button.rect.width/2),centery=button.rect.top+(button.rect.height/2))
        self.screen.blit(text,textpos)
        
    def RenderTextbox(self, textbox):
        # Border
        boxsize = [textbox.textpos.width + self.padding * 2 + self.bordersize * 2, textbox.textpos.height + self.padding * 2 + self.bordersize * 2]
        borderrect = Rect(textbox.textpos.left - self.padding - self.bordersize, textbox.textpos.top - self.padding - self.bordersize, boxsize[0], boxsize[1])

        # Background
        boxsize[0] -= self.bordersize * 2
        boxsize[1] -= self.bordersize * 2
        backgroundrect = Rect(textbox.textpos.left - self.padding, textbox.textpos.top - self.padding, boxsize[0], boxsize[1])

        # Render
        pygame.draw.rect(self.screen, textbox.bordercol, borderrect)
        pygame.draw.rect(self.screen, textbox.bgcol, backgroundrect)
        self.screen.blit(textbox.text, textbox.textpos)

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

# Textbox class
# Requires a rendered text object.
# Optionally, you can provide a rect for the text's position for greater control (e.g. centering)
class Textbox:
    def __init__(self, text, textpos=False):
        if(not textpos):textpos = text.get_rect()
        # Text
        self.text = text
        self.textpos = textpos
        # Colour
        self.bgcol = (0,0,0)
        self.bordercol = (255,0,0)
        self.textcol = (255,255,255)
