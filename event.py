import pygame as pg
import sys 
from vector import Vector
from math import sqrt


class Event:
    # di = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
    #   pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1),
    #   pg.K_d: Vector(1, 0), pg.K_a: Vector(-1, 0),
    #   pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)}

    def __init__(self, si_game):
        self.si_game = si_game 
        self.settings = si_game.settings
        self.stats = si_game.stats
        self.sb = si_game.sb 
        self.game_active = si_game.game_active
        self.ship = si_game.ship

        self.continuous_actions = self.settings.continuous_actions

        self.discrete_actions = self.settings.discrete_actions

        # Title Buttons
        self.play_button = si_game.play_button
        self.high_score_button = si_game.high_score_button
        self.exit_button = si_game.exit_button

        # Game Over Buttons
        self.play_again_button = si_game.play_again_button
        self.title_button = si_game.title_button

        # Prevents Hold Cycles
        self.is_cycling_left = False
        self.is_cycling_right = False

    def check_events(self):
        
        state = self.si_game.game_state[self.si_game.state_index]

        """For discrete control checks"""
        for event in pg.event.get():
            # System-wide quit / exit
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if state == self.si_game.game_state[1]: self.sb.save_high_scores()
                sys.exit()
            
            # Handle based on game state
            if state == self.si_game.game_state[0]:  # Menu State
                self.handle_menu_events(event)

            elif state == self.si_game.game_state[1]:  # In-Game State
                self.handle_game_events(event)

            elif state == self.si_game.game_state[2]:  # In-Game State
                self.handle_scores_events(event)

            elif state == self.si_game.game_state[3]:  # Game Over State
                self.handle_game_over_events(event)

        """For continuous control checks"""
        # We really on need this for the actual game state. . . for now.
        if state == self.si_game.game_state[1]:
            self.control_ship_continuous()

    def handle_menu_events(self, event):
        # If in the Menu State
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            self.check_play_button(mouse_pos)
            self.check_high_score_button(mouse_pos)
            self.check_exit_button(mouse_pos)

        elif event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            self.play_button.set_highlight(mouse_pos)
            self.high_score_button.set_highlight(mouse_pos)
            self.exit_button.set_highlight(mouse_pos)
        
    def handle_game_events(self, event):
        self.control_ship_discrete(event)

    def handle_scores_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            self.check_title_button(mouse_pos)
        elif event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            self.title_button.set_highlight(mouse_pos)

    def handle_game_over_events(self, event):
        # If in the Game Over State
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            self.check_play_again_button(mouse_pos)
            self.check_title_button(mouse_pos)
        elif event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            self.play_again_button.set_highlight(mouse_pos)
            self.title_button.set_highlight(mouse_pos)

    def control_ship_continuous(self):
        keys = pg.key.get_pressed()

        self.ship.v = Vector(0, 0)
        v_input = Vector(0, 0)

        # Movement directions
        if any(keys[key] for key in self.continuous_actions['move_up']):
            v_input += Vector(0, -1)
        if any(keys[key] for key in self.continuous_actions['move_down']):
            v_input += Vector(0, 1)
        if any(keys[key] for key in self.continuous_actions['move_left']):
            v_input += Vector(-1, 0)
        if any(keys[key] for key in self.continuous_actions['move_right']):
            v_input += Vector(1, 0)

        # Focus mode (slow movement modifier)
        focus_mode = any(keys[key] for key in self.continuous_actions['focus_mode'])
        speed = min(self.settings.ship_speed_default / 3, self.settings.ship_speed / 3) if focus_mode else self.settings.ship_speed

        # Apply normalized vector to ship velocity
        self.ship.v += speed * v_input.normal()

        # Firing check - Only active when tap_fire is disabled
        if not self.settings.tap_fire:
            if any(keys[key] for key in self.continuous_actions['fire_hold']):
                self.ship.open_fire()
            else:
                self.ship.cease_fire()

        # keys = pg.key.get_pressed()
        # mods = pg.key.get_mods()

        # self.ship.v = Vector(0, 0)
        # v_input = Vector(0 , 0)

        # # Movement checks
        # if keys[pg.K_UP] or keys[pg.K_w]:
        #     v_input += Vector(0, -1)
        # if keys[pg.K_DOWN] or keys[pg.K_s]:
        #     v_input += Vector(0, 1)
        # if keys[pg.K_LEFT] or keys[pg.K_a]:
        #     v_input += Vector(-1, 0)
        # if keys[pg.K_RIGHT] or keys[pg.K_d]:
        #     v_input += Vector(1, 0)

        # # Normalize the Vector before applying it to the ship # Also check for slow modifier
        # self.ship.v += self.settings.ship_speed * v_input.normal() \
        #         if not mods&pg.KMOD_LSHIFT else min(self.settings.ship_speed_default/3, self.settings.ship_speed/3) * v_input.normal()
        
        # # Firing check - Only procs when tap_fire is disabled.
        # if not self.settings.tap_fire:
        #     if (keys[pg.K_SPACE] or keys[pg.K_KP4] or keys[pg.K_KP5] or keys[pg.K_KP6]):
        #         self.ship.open_fire()
        #     else:
        #         self.ship.cease_fire()

    def control_ship_discrete(self, event):
        if event.type != pg.KEYDOWN:
            return  # Skip if not a key press event

        key = event.key

        # Tap fire (only if enabled)
        if self.settings.tap_fire and key in self.discrete_actions['fire_tap']:
            self.ship.fire_weapon()

        # Cycle weapons
        if key in self.discrete_actions['cycle_weapon_left']:
            self.ship.cycle_weapon(cycle="LEFT")
        elif key in self.discrete_actions['cycle_weapon_right']:
            self.ship.cycle_weapon(cycle="RIGHT")

        # # Ship Tap Fire - Only procs when tap_fire is enabled.
        # if self.settings.tap_fire:
        #     if (event.type == pg.KEYDOWN) and event.key == (pg.K_SPACE or pg.K_KP4 or pg.K_KP5 or pg.K_KP6):
        #         self.ship.fire_weapon()
        
        # # Cycle Weapons
        # if (event.type == pg.KEYDOWN) and event.key == (pg.K_q or pg.K_KP7):
        #     self.ship.cycle_weapon(cycle = "LEFT")

        # if (event.type == pg.KEYDOWN) and event.key == (pg.K_e or pg.K_KP8):
        #     self.ship.cycle_weapon(cycle = "RIGHT")

    def check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.si_game.reset_game()

    def check_high_score_button(self, mouse_pos):
        """Switches to highscore screen."""
        button_clicked = self.high_score_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.si_game.to_high_scores_screen()

    def check_play_again_button(self, mouse_pos):
        """Restart the game when the player clicks Play."""
        button_clicked = self.play_again_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.si_game.reset_game()

    def check_title_button(self, mouse_pos):
        """Sends back to title."""
        button_clicked = self.title_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.si_game.to_title_screen()

    def check_exit_button(self, mouse_pos):
        """Exits the game."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            pg.quit()
            sys.exit()
            

    # def _check_keydown_events(self, event):
    #     key = event.key
    #     if key in Event.di.keys():
    #         self.ship.v += self.settings.ship_speed * Event.di[key]
    #     elif event.key == pg.K_SPACE:
    #         self.ship.open_fire()
    #     elif event.type == pg.KEYUP:
    #         if event.key in Event.di.keys():
    #             self.ship.v = Vector()
    #         elif event.key == pg.K_SPACE:
    #             self.ship.cease_fire()

    # def _check_keyup_events(self, event):
    #     if event.key in Event.di.keys():
    #         self.ship.v = Vector()
    #     elif event.key == pg.K_SPACE:
    #         self.ship.cease_fire()


        
        # System exit and start checks
        # if keys[pg.K_ESCAPE]:
        #     sys.exit()
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         sys.exit()    
            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     mouse_pos = pg.mouse.get_pos()
            #     self.check_play_button(mouse_pos)
            # elif event.type == pg.MOUSEMOTION:
            #     mouse_pos = pg.mouse.get_pos()
            #     self.button.set_highlight(mouse_pos)