import pygame as pg
from colors import *
from fonts import *

class GameOverScreen:
    def __init__(self, si_game):

        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        
        self.title_text_colors = [BLACK, GRAY, WHITE]
        self.title_text_rate = 10
        self.title_text_delay = 1.0 / self.title_text_rate
        self.title_text_timer = 0
        self.title_text_index = 0
        self.title_text_index_opp = self.title_text_index - 1
        self.title_text_color = self.title_text_colors[self.title_text_index]
        self.title_text_color_opp = self.title_text_colors[self.title_text_index_opp]

        # Buttons
        self.play_again_button = si_game.play_again_button
        self.title_button = si_game.title_button
    
    def draw_game_over_title(self):

        self.title_text_timer += self.si_game.dt
        # If enough time has passed:
        if self.title_text_timer >= self.title_text_delay:
            self.title_text_timer = 0
            self.title_text_index += 1
            self.title_text_index %= len(self.title_text_colors)
            self.title_text_color = self.title_text_colors[self.title_text_index]

            self.title_text_index_opp -= 1
            self.title_text_index_opp %= len(self.title_text_colors)
            self.title_text_color_opp = self.title_text_colors[self.title_text_index_opp]

    
        # Set up font
        font = pg.font.Font(PIXEL, 120)

        game_text = font.render(f"GAME", True, self.title_text_color)
        over_text = font.render(f"OVER", True, self.title_text_color_opp)
        
        # Find offset
        spacing = font.size(" ")

        gameRect = game_text.get_rect()
        gameRect.midright = ((self.settings.scr_width / 2) - (spacing[0] / 2), self.settings.scr_height * 0.50 - spacing[1])

        overRect = over_text.get_rect()
        overRect.midleft = ((self.settings.scr_width / 2) + (spacing[0] / 2), self.settings.scr_height * 0.50)

        self.screen.blit(game_text, gameRect)
        self.screen.blit(over_text, overRect)

    def update(self):
        self.screen.fill(BLACK)

        self.draw_game_over_title()
        
        self.play_again_button.draw()
        self.title_button.draw()