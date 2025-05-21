import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint
from colors import *

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien_images/alien0/alien0_base/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien_images/alien1/alien1_base/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien_images/alien2/alien2_base/alien2{n}.png") for n in range(2)]

    ufo_images = [pg.image.load(f"images/alien_images/UFO/UFO_base/UFO.png")]

    alien_boom0 =[pg.image.load(f"images/alien_images/alien0/alien0_explosion/alien0_explosion- ({n}).png") for n in range(1,18)]
    alien_boom1 =[pg.image.load(f"images/alien_images/alien1/alien1_explosion/alien1_explosion- ({n}).png") for n in range(1,18)]
    alien_boom2 =[pg.image.load(f"images/alien_images/alien2/alien2_explosion/alien2_explosion- ({n}).png") for n in range(1,18)]

    ufo_boom = [pg.image.load(f"images/alien_images/UFO/UFO_explosion/UFO_explosion- ({n}).png") for n in range(1,18)]

    alien_type = [{"type" : "Alien",    "color" : "Magenta", "points" : 30,     "sprites_base" : alien_images0, "sprites_boom" : alien_boom0}, 
                  {"type" : "Alien",    "color" : "Cyan",    "points" : 20,     "sprites_base" : alien_images1, "sprites_boom" : alien_boom1}, 
                  {"type" : "Alien",    "color" : "Green",   "points" : 10,     "sprites_base" : alien_images2, "sprites_boom" : alien_boom2},         
                  {"type" : "UFO",      "color" : "Red",     "points" : 100,    "sprites_base" : ufo_images,    "sprites_boom" :   ufo_boom}]

    alien_tile = alien_images2[0].get_rect()

    def __init__(self, si_game, v, type = 0, scale = 1, animation_start = 0, lockstep = False): 
        super().__init__()
        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        
        # Initializing Information and Sprites
        self.info = Alien.alien_type[type % len(Alien.alien_type)]
        self.type = self.info["type"]
        self.color = self.info["color"]
        self.points = self.info["points"]

        # Initializing Sprites
        self.sprites = {
            "base": self.info["sprites_base"][:],
            "boom": self.info["sprites_boom"][:]
            }

        # Scaling
        self.true_scale = self.settings.alien_true_scale * scale
        self.scale_sprites(scale = self.true_scale)

        # Initializing Sprite Timers
        self.alien_base_timer = Timer(images=self.sprites["base"], delta=1000, start_index = animation_start % 2)
        self.alien_explosion_timer = Timer(images=self.sprites["boom"], delta=66, loop_continuously=False, running=False)
        self.timer = self.alien_base_timer
        
        # Initializing Rects
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        # Initializng Location
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Initializing Movement
        self.v = v

        # Alien Guns
        self.guns = [self.rect.center]

        # Specify Laser Attributes
        self.laser_speed = self.settings.alien_laser_speed   
        self.laser_width = self.settings.alien_laser_width
        self.laser_height = self.settings.alien_laser_height  
        self.laser_color = self.settings.alien_laser_color

        self.rng_laser_color = self.settings.rng_laser_color    # Boolean Override

        # Regulate Rate of Fire
        self.rate_of_fire = self.settings.alien_rate_of_fire  # Projectiles per second
        self.fire_interval = 1.0 / self.rate_of_fire  # Time between bullets
        self.fire_accumulator = 0.0  # Time since last fire
        self.weapons_ready = True 

        # Alien Laser -> Maybe we can append this to fleet lasers if necessary.
        self.lasers = pg.sprite.Group()

        # Firing?
        self.firing = False

        # Life and Death Flags
        self.is_active = True
        self.is_dying = False
        self.is_dead = False

        # Flag for checking if score has been counted
        self.score_counted = False

        # Check if sound has already been played once per animation
        self.destruct_sound_played = False

        # Absolute Magnitude
        self.v_magnitude = self.v.magnitude()

        # Lockstep - Toggle for Lockstep Movement / Animation
        self.lockstep = lockstep
        if self.lockstep:
            
            self.step_distance = self.settings.alien_step_distance
            self.step_accumulator = 0.0
            self.step_ready = True
            self.step_interval = 1.0 / self.v_magnitude if self.v_magnitude != 0 else 0  # movement velocity in steps per second
            
            self.alien_base_timer.running = False   # Disabling Default Animation
        
        # Speed Modifier
        self.di_modifier = 1

    def scale_sprites(self, scale):
        for key in self.sprites:
            self.sprites[key] = [
                pg.transform.scale_by(sprite, scale) for sprite in self.info[f"sprites_{key}"]
            ]

    def hit(self):
        if not self.is_dying:
            if self.settings.debug_alien: print('ALIEN HIT! Alien is dying')
            self.is_dying = True
            self.is_active = False
            self.timer = self.alien_explosion_timer
            self.timer.start()

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        # return self.x + self.rect.width >= sr.right or self.x <= 0
        return self.x + (self.rect.width / 2) >= sr.right or self.x <= (self.rect.width / 2)

    def modulate_weapons(self):
        
        # Random Laser Color or Shield Laser Color Override
        if self.rng_laser_color: self.laser_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        
        # RoF and Firing Logic
        if self.firing: # If firing
            if self.weapons_ready:
                self.fire_weapon()
                self.weapons_ready = False
                self.fire_accumulator = 0.0  # Reset accumulator on first shot
            else:
                self.fire_accumulator += self.si_game.dt
                while self.fire_accumulator >= self.fire_interval:
                    self.fire_weapon()
                    self.fire_accumulator -= self.fire_interval
        else:   # To progress cooldown without shooting
            # If the cooldown is active, progress the timer.
            if (not self.weapons_ready) and not (self.fire_accumulator >= self.fire_interval):
                self.fire_accumulator += self.si_game.dt
            # If enough time has passed, re-enable first shot, reset timer.
            elif (not self.weapons_ready) and (self.fire_accumulator >= self.fire_interval):
                self.weapons_ready = True
                self.fire_accumulator = 0

    def fire_weapon(self):
        self.fire_laser(self.guns[0], Vector(0,-1))
    
    def fire_laser(self, gun, v):
        laser = Laser(si_game=self.si_game, gun = gun, color = self.laser_color, v = v,
                      width = self.laser_width, height = self.laser_height)
        self.lasers.add(laser)

    def anchor_guns(self):
        self.guns = [self.rect.center]

    def lockstep_move(self):

        # Magnitude, Cosine, Sin
        self.v_magnitude = self.v.magnitude()
        cos_v = self.v.x / self.v_magnitude
        sin_v = self.v.y / self.v_magnitude

        if self.v_magnitude != 0: # If moving
            if self.is_active: self.step_interval = self.step_distance / (self.v_magnitude * self.di_modifier)
            elif not self.is_active: self.step_interval = self.step_distance / (self.v_magnitude / 2)

            if self.step_ready:
                self.x += cos_v * self.step_distance
                self.y += sin_v * self.step_distance

                self.step_ready = False
                self.step_accumulator_accumulator = 0.0  # Reset accumulator on first step
                if self.is_active: self.timer.advance_frame()
            else:
                self.step_accumulator += self.si_game.dt
                while self.step_accumulator >= self.step_interval:
                    self.x += cos_v * self.step_distance
                    self.y += sin_v * self.step_distance

                    self.step_accumulator -= self.step_interval
                    if self.is_active: self.timer.advance_frame()
                    
        else:   # To progress time without moving
            # If the cooldown is active, progress the timer.
            if (not self.step_ready) and not (self.step_accumulator >= self.step_interval):
                self.step_accumulator += self.si_game.dt
            # If enough time has passed, re-enable first step, reset timer.
            if (not self.step_ready) and (self.step_accumulator >= self.step_interval):
                self.step_ready = True
                self.step_accumulator = 0

    def update(self):
        if self.is_dead: return
        if self.is_dying and self.alien_explosion_timer.finished():
            self.is_dying = False
            self.is_dead = True
            self.destruct_sound_played = False
            if self.settings.debug_alien: print('Alien is dead')
            self.kill()
            return

        # If Healthy
        if self.is_active:
            if not self.lockstep:
                self.x += self.v.x * self.si_game.dt * self.di_modifier 
                self.y += self.v.y * self.si_game.dt * self.di_modifier 
            elif self.lockstep:
                self.lockstep_move()
            
            # Update gun location
            self.anchor_guns()

            # Generic Firing Methods
            self.modulate_weapons()

        elif not self.is_active:
            if self.alien_explosion_timer.index <= 4:
                if not self.lockstep:
                    self.x += self.v.x * self.si_game.dt / 10
                    self.y += self.v.y * self.si_game.dt / 10
                elif self.lockstep:
                    self.lockstep_move()
            
            if not self.destruct_sound_played and self.alien_explosion_timer.index >= 4:
                    self.si_game.sound.play_alien_boom()
                    self.destruct_sound_played = True


        # Update lasers
        self.lasers.update()

        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.draw()

    def draw(self): 
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()




