# UNUSED

# Pygame
import pygame
from pygame import *

if not pygame.font:
    print 'Warning, fonts disabled'
    sys.exit(1)

# Our stuff
from interface import *

#Globals
STATE_MAINMENU  = 0
STATE_PLAYING   = 1
STATE_GAMEOVER  = 2

# Main Menu State class
class MainMenuState:
    def __init__(self, game):
        self.stateid = STATE_MAINMENU
    def render(self, game):
        game.ClearScreen()
        # Title
        text = game.headerfont.render("Nick Cage Film Battle Royale", 1, (255, 0, 0))
        textpos = text.get_rect(centerx=game.width/2, centery=game.height/8)
        game.screen.blit(text, textpos)

        # Start button
        game.interface.RenderButton(game.startbutton)
        game.interface.RenderButton(game.quitbutton)

# Playing state class
class PlayingState:
    def __init__(self, game):
        self.stateid = STATE_PLAYING
    def render(self, game):
        game.ClearScreen()
        # Sprites
        game.enemy_sprites.draw(self.screen)
        game.superenemy_sprites.draw(self.screen)
        game.cage_sprite.draw(self.screen)
        game.rage_sprites.draw(self.screen)
        game.powerup_sprites.draw(self.screen)
        # Render the text (score, month, film) and the charge meter
        game.RenderPlayingInterface()
        # Starting message
        if (curtime <= 2000):
            text = self.headerfont.render("Here come the reviews!", 1, (255,0,0))
            textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
            self.screen.blit(text,textpos)
