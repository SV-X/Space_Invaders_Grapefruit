import sys
import os
import pygame as pg
import time
from colors import *
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from event import Event
from barrier import Barriers
from sound import Sound
from title_screen import TitleScreen
from high_score_screen import HighScoreScreen
from game_over_screen import GameOverScreen

import ctypes

class SpaceInvaders:
    def __init__(self):
        
        pg.init()
        
        # Clock   
        self.clock = pg.time.Clock()
        self.target_FPS = Settings().target_FPS
        self.prev_time = time.time()
        self.dt = (1/self.target_FPS)

        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()

        self.ship = Ship(si_game=self)
        self.fleet = Fleet(si_game=self)
        # self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(si_game=self)

        pg.display.set_caption("Space Invaders")
        self.bg_color = self.settings.bg_color

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # States
        self.game_state = {0 : "Title",
                           1 : "Playing",
                           2 : "High Score",
                           3 : "Game Over"}
        self.state_index = 0

        # Buttons
        self.play_button = Button(self, "Play Game", (self.screen.get_rect().centerx, self.settings.scr_height * 0.725))
        self.high_score_button = Button(self, "High Scores", (self.screen.get_rect().centerx, self.settings.scr_height * 0.825))
        
        self.play_again_button = Button(self, "Try Again?", (self.screen.get_rect().centerx, self.settings.scr_height * 0.725))
        self.title_button = Button(self, "Title", (self.screen.get_rect().centerx, self.settings.scr_height * 0.825))

        self.exit_button = Button(self, "System Exit", (self.screen.get_rect().centerx, self.settings.scr_height * 0.925))
        
        # Screens
        self.title_screen = TitleScreen(si_game=self)
        self.hs_screen = HighScoreScreen(si_game=self)
        self.go_screen = GameOverScreen(si_game=self)

        # Events
        self.event = Event(self)

    def to_title_screen(self):
        self.state_index = 0

        pg.mixer.music.fadeout(100)
        self.sound.load_game_bgm()
        self.sound.play_background()

    def to_game_screen(self):
        self.state_index = 1

    def to_high_scores_screen(self):
        self.state_index = 2

        pg.mixer.music.fadeout(100)
        self.sound.load_turbo_bgm()
        self.sound.play_background()

    def game_over(self):
        self.ship.lasers.empty()
        self.fleet.aliens.empty()
        
        print("Game over!")
        # self.sound.stop_background()
        self.sound.play_gameover()

        self.sound.load_gameover_bgm()
        self.sound.play_background()

        self.sb.save_high_scores()
        self.state_index = 3
        pg.mouse.set_visible(True)        

    def reset_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        # self.game_active = True

        pg.mixer.music.fadeout(100)
        self.sound.load_game_bgm_v2()
        self.sound.play_background()

        self.barriers.reset()
        self.ship.initialize_ship()
        self.fleet.initialize_fleet()
        pg.mouse.set_visible(False)
        self.to_game_screen()

    def update_clock(self):
        self.clock.tick(self.target_FPS)
        # self.dt = (1/self.target_FPS)
    
    def update_dynamic_clock(self):
        self.clock.tick(self.target_FPS)
        self.now = time.time()
        self.dt = self.now - self.prev_time
        self.prev_time = self.now        

    def check_states(self):
        pass

    def check_fail_states(self):
        if self.ship.destroyed or self.fleet.check_bottom():
            self.ship.ship_lose_life()
            self.ship.reset_ship()
            self.fleet.aliens.empty()
            self.fleet.create_fleet()
            time.sleep(0.5) 
        
        if not self.ship.has_lives:
            self.game_over()

    def run_game(self):
        self.running = True
        # self.game_active = False
        self.to_title_screen()

        while self.running:
            self.update_clock()
            self.event.check_events()
            
            if self.game_state[self.state_index] == self.game_state[0]:
                # self.screen.fill(BLACK)
                self.title_screen.update()

            elif self.game_state[self.state_index] == self.game_state[1]:
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()
                self.check_fail_states()

            elif self.game_state[self.state_index] == self.game_state[2]:
                # self.screen.fill(BLACK)
                self.hs_screen.update()
                # self.title_button.draw()

            elif self.game_state[self.state_index] == self.game_state[3]:
                # self.screen.fill(BLACK)
                self.go_screen.update()
    
            pg.display.flip()
        sys.exit()

# This is to ensure Windows does not mess with the display.
def windows_bugger_off():
    # If Windows:
    if os.name == "nt":
        try:
            # Tell Windows to bugger off.
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            # Do nothing
            pass   

if __name__ == '__main__':
    windows_bugger_off()

    sig = SpaceInvaders()
    sig.run_game()
