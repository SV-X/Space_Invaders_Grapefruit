from colors import*
import pygame as pg

class Settings:

    def __init__(self):
        #Screen Settings
        # self.scr_width = 1200
        # self.scr_height = 800

        self.scr_width = 1920
        self.scr_height = 1080

        self.bg_color = BLACK
        self.w_h = (self.scr_width, self.scr_height)

        # Clock Settings
        self.target_FPS = 60

        # Controls
        self.initialize_controls_default()

        # Resolution Scale
        self.resoultion_scale = self.scr_height / 1080

        # Relative Scale
        self.fighter_image_scale = 3 * 1.5
        self.alien_image_scale = 5 * 1.5

        # True Scale
        self.fighter_true_scale = self.fighter_image_scale * self.resoultion_scale
        self.alien_true_scale = self.alien_image_scale * self.resoultion_scale

        # Ship Settings

        # Ship Speed Settings
        self.ship_speed_default = 300.0 * self.fighter_image_scale * self.resoultion_scale

        # Ship Laser Settings
        self.laser_speed_default = 140 * self.fighter_image_scale * self.resoultion_scale
        self.laser_width = 1 * self.fighter_image_scale * self.resoultion_scale
        self.laser_height_default = 9 * self.fighter_image_scale * self.resoultion_scale
        self.laser_color = GREEN
        self.shield_laser_color = True

        # Ship Weapon Settings
        self.rate_of_fire = 30

        # Ship Outline Colors
        self.shield_color = GREEN
        self.shield_flash_color = CYAN
        self.shield_flash_colors = [self.shield_color, self.shield_flash_color]

        # Ship Ghost Colors
        self.ghost_color = EMERALD
        self.ghost_flash_color = SKYBLUE
        self.ghost_flash_colors = [self.ghost_color, self.ghost_flash_color]

        # Ship Flash
        self.ship_flash_rate = 10

        # Ship Shield Colors
        self.shield_colors = {
            "HYPER":    {"Shield":[RED, ORANGE, YELLOW, GRASS, GREEN, SEA, CYAN, AQUA, BLUE, PURPLE, MAGENTA, ROSE],
                         "Ghost":[RED, ORANGE, YELLOW, GRASS, GREEN, SEA, CYAN, AQUA, BLUE, PURPLE, MAGENTA, ROSE]},
            "Strong":   {"Shield":[GREEN, CYAN],   "Ghost":[EMERALD, SKYBLUE]},
            "Medium":   {"Shield":[BLUE, MAGENTA], "Ghost":[DEEPSEA, LAVENDER]},
            "Weak":     {"Shield":[RED, YELLOW],   "Ghost":[FIRE, SUN]},
            "GONE":     {"Shield":[WHITE, BLACK],  "Ghost":[GRAY]}
            }

        # Ship Shields
        self.max_shield_health = 3
        self.shield_recharge_delay = 5  # Minimum time after taking before shield can recharge
        self.shield_charge_rate = 1/3

        # Ship Lives
        self.ship_limit = 3

        # RNG Settings
        self.rng_laser_color = False
        self.continuous_rng_laser_color = False
        self.rng_shield_color = False
        self.rng_ghost_color = False

        # Dynamic Scales
        self.speedup_scale = 1.1
        self.score_scale = 1.1

        # Alien Speed Settings
        self.alien_speed_default = 12.0 * self.alien_image_scale * self.resoultion_scale
        self.alien_step_distance = 4 * self.alien_image_scale * self.resoultion_scale

        # Alien Laser Settings
        self.alien_laser_speed = 3 * self.alien_image_scale * self.resoultion_scale
        self.alien_laser_width = 1 * self.alien_image_scale * self.resoultion_scale
        self.alien_laser_height = 1 * self.alien_image_scale * self.resoultion_scale
        self.alien_laser_color = RED

        # Alien Weapon Settings
        self.alien_rate_of_fire = 12

        # UFO Spawn Settings
        self.ufo_min_time = 0
        self.ufo_max_time = 60

        # Fleet Settings
        self.fleet_drop_distance = 4 * self.alien_image_scale * self.resoultion_scale
        self.alien_columns = 11
        self.alien_rows = 5
        self.fleet_rate_of_fire = 1
        self.fleet_max_speed = 9.0

        # Dynamic Settings
        self.increase_dynamic_speed = True
        self.initialize_dynamic_settings()

        # Traditional Tap Fire
        self.tap_fire = False

        # Debug Settings
        self.debug = False
        self.debug_ship = False
        self.debug_alien = False
        self.debug_UFO = False
        self.debug_fleet = False
        self.debug_barrier = False

    def initialize_controls_default(self):
        self.continuous_actions = {
            'move_up': [pg.K_UP, pg.K_w],
            'move_down': [pg.K_DOWN, pg.K_s],
            'move_left': [pg.K_LEFT, pg.K_a],
            'move_right': [pg.K_RIGHT, pg.K_d],
            'fire_hold': [pg.K_SPACE, pg.K_KP4, pg.K_KP5, pg.K_KP6],
            'focus_mode': [pg.K_LSHIFT],  # Modifier for precision movement
            }

        self.discrete_actions = {
            'fire_tap': [pg.K_SPACE, pg.K_KP4, pg.K_KP5, pg.K_KP6],
            'cycle_weapon_left': [pg.K_q, pg.K_KP7],
            'cycle_weapon_right': [pg.K_e, pg.K_KP8],
            }

    def initialize_dynamic_settings(self):
        
        # Ship
        self.ship_speed = self.ship_speed_default
        self.laser_speed = self.laser_speed_default
        self.laser_height = self.laser_height_default # Laser Compensation

        # Aliens
        self.alien_speed = self.alien_speed_default
        # self.alien_points = 50
        self.alien_points_multiplier = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.laser_height *= self.speedup_scale # Laser Compensation

        self.alien_speed *= self.speedup_scale

        # self.alien_points = int(self.alien_points * self.score_scale)
        self.alien_points_multiplier *= self.score_scale


def main():
    print('\n*** message from settings.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()