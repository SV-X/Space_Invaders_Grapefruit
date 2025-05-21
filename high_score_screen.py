import pygame as pg
from colors import *
from fonts import *
class HighScoreScreen:
    def __init__(self, si_game):

        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        self.sb = si_game.sb
        
        # High Score Text Attributes
        self.high_score_colors = self.settings.shield_colors["HYPER"]["Shield"]
        self.high_score_color_rate = 10
        self.high_score_color_delay = 1.0 / self.high_score_color_rate
        self.high_score_color_timer = 0
        self.high_score_color_index = 0
        self.high_score_color = self.high_score_colors[self.high_score_color_index]

        # Rank Score Attributes
        self.rank_colors = [GREEN, ORANGE]
        self.rank_color_rate = 1
        self.rank_color_delay = 1.0 / self.rank_color_rate
        self.rank_color_timer = 0
        self.rank_color_index = 0
        self.score_color_index = self.rank_color_index + 1
        self.rank_color = self.rank_colors[self.rank_color_index]
        self.score_color = self.rank_colors[self.score_color_index]

        # Buttons
        self.title_button = si_game.title_button
    
    def draw_high_score_title(self):

        self.high_score_color_timer += self.si_game.dt
        # If enough time has passed:
        if self.high_score_color_timer >= self.high_score_color_delay:
            self.high_score_color_timer = 0
            self.high_score_color_index += 1
            self.high_score_color_index %= len(self.high_score_colors)
            self.high_score_color = self.high_score_colors[self.high_score_color_index]
        
        # Set up font
        font = pg.font.Font(PIXEL, 90)
        high_score_color = font.render(f"HIGH SCORES", True, self.high_score_color)
        
        textRect = high_score_color.get_rect()
        textRect.center = (self.settings.scr_width / 2, self.settings.scr_height * 0.15)

        self.screen.blit(high_score_color, textRect)


    def draw_high_scores(self):
        self.rank_color_timer += self.si_game.dt
        # If enough time has passed:
        if self.rank_color_timer >= self.rank_color_delay:
            self.rank_color_timer = 0
            self.rank_color_index += 1
            self.rank_color_index %= len(self.rank_colors)
            self.rank_color = self.rank_colors[self.rank_color_index]
            
            self.score_color_index += 1
            self.score_color_index %= len(self.rank_colors)
            self.score_color = self.rank_colors[self.score_color_index]

        # Set up font
        font = pg.font.Font(PIXEL, 50)

        text_height = font.get_height()  # Height of each score

        # Calculate starting position (centered vertically)
        start_y = self.settings.scr_height * 0.25

        # Fixed X coordinate for the enumerated numbers and scores
        rank_x = self.settings.scr_width * 0.39  # Rank for the score (all numbers will align here)
        score_x = self.settings.scr_width * 0.59  # Fixed position for the score text (offset by a constant)

        for i, score in enumerate(self.sb.high_scores):
            
            # Render the number and score text (both left-aligned with fixed X coordinates)
            number_text = font.render(f"{i + 1}.", True, self.rank_color)
            score_color = font.render(f"{score}", True, self.score_color)
            
            # For Alignment
            numRect = number_text.get_rect()
            numRect.midright = (rank_x, start_y + i * text_height)

            scoreRect = number_text.get_rect()
            scoreRect.midleft = (score_x, start_y + i * text_height)

            # Position the number and the score text
            self.screen.blit(number_text, numRect)
            self.screen.blit(score_color, scoreRect)

    def update(self):
        self.screen.fill(BLACK)
        
        self.draw_high_score_title()
        self.draw_high_scores()
        self.title_button.draw()