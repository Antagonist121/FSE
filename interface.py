# Pygame
import pygame
from pygame import *

if not pygame.font:
    print 'Warning, fonts disabled'
    sys.exit(1)

# Interface class
class Interface:
    def __init__(self, screen):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.buttonpadding = 10 # Gap between buttons
        self.padding = 5 # General padding around elements
    def RenderButton(self, button):
        pygame.draw.rect(self.screen, (255,0,0), button.rect)
        text = self.font.render(button.message, 1, (0,0,0))
        textpos = text.get_rect(centerx=button.rect.left+(button.rect.width/2),centery=button.rect.top+(button.rect.height/2))
        self.screen.blit(text,textpos)

# Button class
class Button:
    def __init__(self, rect, message):
        self.rect = rect
        self.message = message
    def Clicked(self, mousepos):
        if(mousepos[0] < self.rect.left or mousepos[0] > self.rect.right):return False
        if(mousepos[1] < self.rect.top or mousepos[1] > self.rect.bottom):return False
        return True
