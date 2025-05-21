import pygame as pg
from colors import *
from fonts import *
from random import uniform
from ship import Ship
from alien import Alien
from ufo import UFO
from vector import Vector

from cycle_return import CycleReturn
from cycle_boolean import CycleBoolean

class TitleScreen:
    def __init__(self, si_game):

        self.si_game = si_game
        self.screen = si_game.screen
        self.screen_rect = si_game.screen.get_rect()
        self.settings = si_game.settings
        
        self.title_text_colors = [GREEN, MAGENTA]

        self.space_colors = CycleReturn(si_game=self.si_game, group = self.title_text_colors, rate = 10, member_index=0)
        self.invaders_colors = CycleReturn(si_game=self.si_game, group = self.title_text_colors, rate = 10, member_index=1)
        self.title_text_color = self.space_colors.update()
        self.title_text_color_alt = self.invaders_colors.update()

        # Buttons
        self.play_button = si_game.play_button
        self.high_score_button = si_game.high_score_button
        self.exit_button = si_game.exit_button
        
        self.initialize_title_title()
        self.initialize_title_ships()
        self.initialize_title_aliens()


    def initialize_title_title(self):
        self.title_text_color = self.space_colors.update()
        self.title_text_color_alt = self.invaders_colors.update()

        # Set up font
        self.font_title = pg.font.Font(PIXEL, 90)

        space_text = self.font_title.render(f"SPACE ", True, self.title_text_color)
        invaders_text = self.font_title.render(f"INVADERS", True, self.title_text_color_alt)
        
        # Find offset
        difference = invaders_text.get_width() - space_text.get_width()

        self.spaceRect = space_text.get_rect()
        self.spaceRect.midright = ((self.settings.scr_width / 2) - (difference / 2), self.settings.scr_height * 0.175)

        self.invadersRect = invaders_text.get_rect()
        self.invadersRect.midleft = ((self.settings.scr_width / 2) - (difference / 2), self.settings.scr_height * 0.175)

        self.screen.blit(space_text, self.spaceRect)
        self.screen.blit(invaders_text, self.invadersRect)


    def initialize_title_ships(self):
        self.title_ship = Ship(si_game=self.si_game)
        self.title_ship.x, self.title_ship.y = self.screen.get_rect().center
        self.title_ship_u = Ship(si_game=self.si_game)
        self.title_ship_u.x, self.title_ship_u.y = self.screen.get_rect().center

        self.can_act = CycleBoolean(si_game=self.si_game, rate = 1)
        self.vector = Vector(0,0)

    
    def initialize_title_aliens(self):
        # Aliens for Menu
        self.magenta_alien = Alien(si_game=self.si_game, v=Vector(0,0), type = 0)
        self.cyan_alien = Alien(si_game=self.si_game, v=Vector(0,0), type = 1)
        self.green_alien = Alien(si_game=self.si_game, v=Vector(0,0), type = 2)
        self.ufo_alien = UFO(si_game=self.si_game, v=Vector(0,0), type=3)
        
        self.font_aliens = pg.font.Font(PIXEL, 50)
        self.spacing = self.font_aliens.size(" ")

        columnL = self.settings.scr_width * 0.425
        columnM = self.settings.scr_width * 0.50
        columnR = self.settings.scr_width * 0.575

        self.rowUFO = self.settings.scr_height * 0.30
        self.rowMagenta = self.settings.scr_height * 0.40
        self.rowCyan = self.settings.scr_height * 0.50
        self.rowGreen = self.settings.scr_height * 0.60

        self.ufo_alien.x, self.ufo_alien.y = (columnL, self.rowUFO)
        self.magenta_alien.x, self.magenta_alien.y = (columnL, self.rowMagenta)
        self.cyan_alien.x, self.cyan_alien.y = (columnL, self.rowCyan)
        self.green_alien.x, self.green_alien.y = (columnL, self.rowGreen)

        # Equals Text For Menu
        self.equals_text = self.font_aliens.render(f" = ", True, WHITE)
        
        # Rects for Spacing
        self.equalsUFORect = self.equals_text.get_rect()
        self.equalsMagentaRect = self.equals_text.get_rect()
        self.equalsCyanRect = self.equals_text.get_rect()
        self.equalsGreenRect = self.equals_text.get_rect()

        # Positioning Rects
        self.equalsUFORect.center = (columnM, self.rowUFO)
        self.equalsMagentaRect.center = (columnM, self.rowMagenta)
        self.equalsCyanRect.center = (columnM, self.rowCyan)
        self.equalsGreenRect.center = (columnM, self.rowGreen)

        # Scores Text For Menu
        self.ufo_points = self.font_aliens.render(f"???", True, WHITE)
        self.magenta_points = self.font_aliens.render(f"{self.magenta_alien.points}", True, MAGENTA)
        self.cyan_points = self.font_aliens.render(f"{self.cyan_alien.points}", True, CYAN)
        self.green_points = self.font_aliens.render(f"{self.green_alien.points}", True, GREEN)

        # Rects for Spacing
        self.pointsUFORect = self.ufo_points.get_rect()
        self.pointsMagentaRect = self.magenta_points.get_rect()
        self.pointsCyanRect = self.cyan_points.get_rect()
        self.pointsGreenRect = self.green_points.get_rect()

        # Positioning Rects
        self.pointsUFORect.center = (columnR, self.rowUFO)
        self.pointsMagentaRect.center = (columnR, self.rowMagenta)
        self.pointsCyanRect.center = (columnR, self.rowCyan)
        self.pointsGreenRect.center = (columnR, self.rowGreen)

        # Colors
        self.hyper = self.settings.shield_colors["HYPER"]["Shield"]
        self.ufo_colors = CycleReturn(si_game=self.si_game, group = self.hyper, rate = 10, member_index=0)

    def update_title_title(self):

        self.title_text_color = self.space_colors.update()
        self.title_text_color_alt = self.invaders_colors.update()

        space_text = self.font_title.render(f"SPACE ", True, self.title_text_color)
        invaders_text = self.font_title.render(f"INVADERS", True, self.title_text_color_alt)

        self.screen.blit(space_text, self.spaceRect)
        self.screen.blit(invaders_text, self.invadersRect)

    def update_title_ships(self):
        if self.can_act.act():
            vector = Vector(uniform(-1,1), uniform(-1,1)).normal()
            self.title_ship.v = self.settings.ship_speed * vector
            self.title_ship_u.v = self.settings.ship_speed * - vector

        self.title_ship.update()
        self.title_ship_u.update()
    
    def update_title_aliens(self):
        self.green_alien.update()
        self.cyan_alien.update()
        self.magenta_alien.update()
        self.ufo_alien.update()

        self.ufo_color = self.ufo_colors.update()

        ufo_points = self.font_aliens.render(f"???", True, self.ufo_color)
        
        self.screen.blit(ufo_points, self.pointsUFORect)
        self.screen.blit(self.magenta_points, self.pointsMagentaRect)
        self.screen.blit(self.cyan_points, self.pointsCyanRect)
        self.screen.blit(self.green_points, self.pointsGreenRect)

        self.screen.blit(self.equals_text, self.equalsUFORect)
        self.screen.blit(self.equals_text, self.equalsMagentaRect)
        self.screen.blit(self.equals_text, self.equalsCyanRect)
        self.screen.blit(self.equals_text, self.equalsGreenRect)


    def update(self):
        self.screen.fill(BLACK)
        
        self.update_title_title()
        self.update_title_ships()
        self.update_title_aliens()
        
        self.play_button.draw()
        self.high_score_button.draw()
        self.exit_button.draw()