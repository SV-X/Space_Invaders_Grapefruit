import pygame as pg
import pygame.font
from colors import *
from fonts import *

class Button:
    """A class to build buttons for the game."""
    def __init__(self, si_game, msg, pos):
        """Initialize button attributes."""
        self.screen = si_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 55
        self.msg = msg
        self.font = pygame.font.Font(PIXEL, 48)
        self.text_colors = [WHITE, DARK_GREEN]
        self.highlighted = False
        self.colors = [GREEN, ORANGE]
        self.position = pos

        self.spacing = self.font.size(" ")[0]

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.position

        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def color(self): return self.colors[0 if not self.highlighted else 1]
    """new function for returning Titan colors when mouse-over"""

    def text_color(self): return self.text_colors[0 if not self.highlighted else 1]

    def set_highlight(self, pos): 
        """sets highlight for Titan-colored buttons when mouse over"""
        r = self.rect
        self.highlighted = pg.Rect.collidepoint(r, pos)
        self.prep_msg(self.msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg = msg
        self.msg_image = self.font.render(msg, True, self.text_color(),
                self.color())
        self.msg_image_rect = self.msg_image.get_rect()
        self.width = self.msg_image_rect.width + self.spacing
        self.rect.width = self.width
        self.rect.center = self.position
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.color(), self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)