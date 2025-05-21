import pygame as pg
from vector import Vector
from point import Point
from laser import Laser
from timer import Timer
from time import sleep
from pygame.sprite import Sprite
from outline import get_outline

from random import randint

class Ship(Sprite):
    grapefruit_base = [pg.image.load(f"images/fighter_images/fighter_base/fighter-{n}.png") for n in range(1)]
    grapefruit_boom = [pg.image.load(f"images/fighter_images/fighter_explosion/fighter_explosion- ({n}).png") for n in range(1,63)]
    grapefruit_damage = [pg.image.load(f"images/fighter_images/fighter_hit/fighter_hit-{n}.png") for n in range(0,2)]

    fighter_info = [{"name": "Grapefruit", "type" : "fighter", "sprites_base" : grapefruit_base, "sprites_boom" : grapefruit_boom, "sprites_damage" : grapefruit_damage}]

    def __init__(self, si_game, v=Vector(), type = 0, scale = 1):
        super().__init__()
        # General Initializations
        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        self.screen_rect = si_game.screen.get_rect()
        self.stats = si_game.stats
        self.sb = None

        # Information
        self.info = Ship.fighter_info[type % len(Ship.fighter_info)]

        # Initializing Sprites
        self.sprites = {
            "base": self.info["sprites_base"][:],
            "damage": self.info["sprites_damage"][:],
            "boom": self.info["sprites_boom"][:]
            }

        # Scaling
        self.true_scale = self.settings.fighter_true_scale * scale
        self.scale_sprites(scale = self.true_scale)

        # Initializing Sprite Timers
        self.ship_base_timer = Timer(images=self.sprites["base"], delta=33, running=False)
        self.ship_damage_timer = Timer(images=self.sprites["damage"], delta=66)
        self.ship_explosion_timer = Timer(images=self.sprites["boom"], delta=33, loop_continuously=False, running=False)
        self.timer = self.ship_base_timer

        # Initializing Image and Rects
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        #Initializing Location
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        
        # For Bounds Calculations
        self.ship_width = self.rect.width
        self.ship_height = self.rect.height

        # Initializing Shield
        self.shield_color = self.settings.shield_color
        self.image_shield = get_outline(self.image, color = self.shield_color, threshold = 100, alpha = 255)
        self.image_shield_rect = self.image_shield.get_rect()
        self.image_shield_rect.center = self.rect.center

        # Shield Flash
        self.shield_flash_colors = self.settings.shield_flash_colors
        self.shield_flash_rate = self.settings.ship_flash_rate
        self.shield_flash_delay = 1.0 / self.shield_flash_rate
        self.shield_flash_timer = 0
        self.shield_flash_index = 0

        # Initializing Ghost
        self.ghost_color = self.settings.ghost_color
        self.image_ghost = get_outline(self.image, color = self.ghost_color, threshold = 100, alpha = 255)
        self.image_ghost_rect = self.image_ghost.get_rect()
        self.image_ghost_rect.center = self.rect.center

        # Ghost Flash
        self.ghost_flash_colors = self.settings.ghost_flash_colors
        self.ghost_flash_rate = self.settings.ship_flash_rate
        self.ghost_flash_delay = 1.0 / self.ghost_flash_rate
        self.ghost_flash_timer = 0
        self.ghost_flash_index = 1

        # Initializing Shield Attributes
        self.shield_colors = self.settings.shield_colors
        self.max_shield_health = self.settings.max_shield_health
        self.shield_health = self.max_shield_health
        self.shield_recharge_delay = self.settings.shield_recharge_delay  # Minimum time after taking before shield can recharge
        self.shield_charge_rate = self.settings.shield_charge_rate # per second
        self.shield_recharge_timer = 0
        
        # Initializing Invulnerability Attributes
        self.is_invulnerable = False
        self.invulnerability_time_window = 1 # Seconds
        self.invulnerability_timer = 0

        # Initializing Velocity
        self.v = v

        # Initializing Laser Group to Store Lasers for Calculations
        self.lasers = pg.sprite.Group()

        # Initializing Firing Flag
        self.firing = False

        # Separate guns -> Since I cannot point to tuples, I will be setting and updating them via method.
        self.guns = [self.rect.center]

        # Cycling Through Weapons
        self.weapon_guide = {"Wide Laser"   :   self.fire_wide_laser,
                             "Tri Laser"    :   self.fire_tri_laser,
                             "V Laser"      :   self.fire_v_laser,
                             "Cross Laser"  :   self.fire_cross_laser}
        self.weapon_names = list(self.weapon_guide.keys())
        self.weapon_functions = list(self.weapon_guide.values())
        self.weapon_index = 0

        # Specify Laser Attributes
        self.laser_speed = self.settings.laser_speed    # Dynamic
        self.laser_width = self.settings.laser_width
        self.laser_height = self.settings.laser_height  # Dynamic
        self.laser_color = self.settings.laser_color
        self.shield_laser_color = self.settings.shield_laser_color
        self.rng_laser_color = self.settings.rng_laser_color    # Boolean Override

        # Regulate Rate of Fire
        self.rate_of_fire = self.settings.rate_of_fire  # Projectiles per second
        self.fire_interval = 1.0 / self.rate_of_fire  # Time between bullets
        self.fire_accumulator = 0.0  # Time since last fire
        self.weapons_ready = True 

        # Life and Death Flags
        self.is_dying = False
        self.destroyed = False
        self.has_lives = True
        
        # Check if sound has already been played once per animation
        self.destruct_sound_played = False

        # Modifies Direction and RoF for Specific Events
        self.di_modifier = 1
        self.rof_modifier = 1
    
    def scale_sprites(self, scale):
        for key in self.sprites:
            self.sprites[key] = [
                pg.transform.scale_by(sprite, scale) for sprite in self.info[f"sprites_{key}"]
            ]

    def set_sb(self, sb): self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()
        
        # Resetting Flags
        self.is_invulnerable = False
        self.destroyed = False
        
        # Resetting Explosion Timer Index and Ship Sprite.
        self.ship_explosion_timer.index = 0
        self.timer = self.ship_base_timer

        # Resetting Cooldowns
        self.invulnerability_timer = 0
        self.shield_recharge_timer = 0

        # Resetting Health
        self.shield_health = self.max_shield_health
        self.manage_shield_colors()

    def initialize_ship(self):
        self.max_shield_health = self.settings.max_shield_health
        self.update_dynamic_settings()
        self.reset_ship()
        self.has_lives = True

    def center_ship(self):         
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def bound(self):
        x, y, scr_r = self.x, self.y, self.screen_rect
        # self.x = max(0, min(x, scr_r.width - self.rect.width)) 
        # self.y = max(0, min(y, scr_r.height - self.rect.height))
        self.x = max(self.ship_width / 2, min(x, scr_r.width - (self.ship_width / 2)-1)) 
        self.y = max(self.ship_height / 2, min(y, scr_r.height - (self.ship_height / 2)-1))
    
    def modulate_weapons(self):
        
        # Random Laser Color or Shield Laser Color Override
        if self.rng_laser_color: self.laser_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        elif self.shield_laser_color: self.laser_color = self.shield_flash_colors[self.shield_flash_index%len(self.shield_flash_colors)]
        
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
            if (not self.weapons_ready) and (self.fire_accumulator >= self.fire_interval):
                self.weapons_ready = True
                self.fire_accumulator = 0

    def fire_laser(self, gun, v):
        laser = Laser(si_game=self.si_game, gun = gun, color = self.laser_color, v = v,
                      width = self.laser_width, height = self.laser_height)
        self.lasers.add(laser)
        
    def open_fire(self): self.firing = True 

    def cease_fire(self): self.firing = False

    def fire_weapon(self):
        self.weapon_functions[self.weapon_index]()

    def cycle_weapon(self, cycle):
        if cycle == "RIGHT":
            self.weapon_index += 1
        elif cycle == "LEFT":
            self.weapon_index -= 1
        self.weapon_index %= len(self.weapon_guide)

        print("Weapon Active:", self.weapon_names[self.weapon_index])

    def fire_wide_laser(self):
        for gun in self.guns.values():
            self.fire_laser(gun, Vector(0,1))
    
        self.si_game.sound.play_laser_fire_b()

    def fire_v_laser(self):
        self.fire_laser(self.guns["GunRT"], Vector(1,1))
        self.fire_laser(self.guns["GunLT"], Vector(-1,1))
        self.fire_laser(self.guns["GunRB"], Vector(1,1))
        self.fire_laser(self.guns["GunLB"], Vector(-1,1))
        
        self.si_game.sound.play_laser_fire_c()

    def fire_tri_laser(self):
        self.fire_laser(self.guns["GunRT"], Vector(0,1))
        self.fire_laser(self.guns["GunLT"], Vector(0,1))
        self.fire_laser(self.guns["GunRB"], Vector(1,1))
        self.fire_laser(self.guns["GunLB"], Vector(-1,1))
        
        self.si_game.sound.play_laser_fire_a()

    def fire_cross_laser(self):
        self.fire_laser(self.guns["GunRT"], Vector(1,1))
        self.fire_laser(self.guns["GunLT"], Vector(-1,1))
        self.fire_laser(self.guns["GunRB"], Vector(-1,-1))
        self.fire_laser(self.guns["GunLB"], Vector(1,-1))
        
        self.si_game.sound.play_laser_fire_d()

    # Since we can't point to tuples. :(
    def anchor_guns(self):
        self.guns = {"GunRT" : tuple(map(sum, zip(self.rect.center, (self.true_scale * 3,self.true_scale * -13)))),
                     "GunLT" : tuple(map(sum, zip(self.rect.center, (self.true_scale * -3,self.true_scale * -13)))),
                     "GunRB" : tuple(map(sum, zip(self.rect.center, (self.true_scale * 6,self.true_scale * -5)))),
                     "GunLB" : tuple(map(sum, zip(self.rect.center, (self.true_scale * -6,self.true_scale * -5))))}

    def ship_hit(self, damage = 1):
        if self.is_invulnerable:
            if self.settings.debug_ship: print("CANT STOP WONT STOP")
        if not self.is_invulnerable:
            if self.settings.debug_ship: print("Taking Damage")

            # Take damage -> Start Invulnerability
            self.adjust_shield_health(- damage)
            self.is_invulnerable = True
            self.invulnerability_timer = self.invulnerability_time_window

            # Visual and Audio Feedback
            if not self.is_dying:
                self.timer = self.ship_damage_timer     # Have to check to not overwrite explosion
                self.si_game.sound.play_ship_hit()      # Don't want damage spam either.
            
            # Prep shields for recharge
            self.shield_recharge_timer = self.shield_recharge_delay
            if self.settings.debug_ship: print("Invulnerability Timer: ", self.invulnerability_timer)
            if self.settings.debug_ship: print("Time until recharge: ", self.shield_recharge_timer)
            if self.settings.debug_ship: print("Current Shield Health: ", self.shield_health)
            
            # If hit with 0 shields, initiate destruct sequence
            if self.shield_health < 0:
                self.initiate_destruction_sequence()
    
    def update_invulnerability(self):
        if self.is_invulnerable and self.invulnerability_timer > 0:
            self.invulnerability_timer -= self.si_game.dt
            self.invulnerability_timer = max(self.invulnerability_timer, 0)
            if self.settings.debug_ship: print("Invulnerability Timer: ", self.invulnerability_timer)
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.timer = self.ship_base_timer

    def update_shields(self):
        self.charge_shields()
        self.manage_shield_colors()

    def charge_shields(self):
        if self.shield_recharge_timer > 0:
            self.shield_recharge_timer -= self.si_game.dt
            self.shield_recharge_timer = max(self.shield_recharge_timer, 0)
            if self.settings.debug_ship: print("Time until recharge: ", self.shield_recharge_timer)
        elif self.shield_health < self.max_shield_health and self.shield_recharge_timer <= 0:
            self.shield_health += self.shield_charge_rate * self.si_game.dt
            self.shield_health = min(self.shield_health, self.max_shield_health)
            if self.settings.debug_ship: print("Shield Charging: ", self.shield_health)

    def manage_shield_colors(self):
        if self.shield_health >= 4:
            self.shield_flash_colors = self.shield_colors["HYPER"]["Shield"]
            self.ghost_flash_colors = self.shield_colors["HYPER"]["Ghost"]
        elif self.shield_health >= 3:
            self.shield_flash_colors = self.shield_colors["Strong"]["Shield"]
            self.ghost_flash_colors = self.shield_colors["Strong"]["Ghost"]
        elif self.shield_health >= 2:
            self.shield_flash_colors = self.shield_colors["Medium"]["Shield"]
            self.ghost_flash_colors = self.shield_colors["Medium"]["Ghost"]
        elif self.shield_health >= 1:
            self.shield_flash_colors = self.shield_colors["Weak"]["Shield"]
            self.ghost_flash_colors = self.shield_colors["Weak"]["Ghost"]
        else:
            self.shield_flash_colors = self.shield_colors["GONE"]["Shield"]
            self.ghost_flash_colors = self.shield_colors["GONE"]["Ghost"]
    
    def adjust_max_shield(self, amount = 0):
        self.max_shield_health = max(self.max_shield_health + amount, 9)

    def adjust_shield_health(self, amount = 0):
        self.shield_health += amount

    def initiate_destruction_sequence(self):
        self.is_invulnerable = False
        if not self.is_dying:
            print('CRITICAL FAILURE! SYSTEM OVERLOADED!')
            self.is_dying = True
            self.timer = self.ship_explosion_timer
            self.timer.start()
            self.si_game.sound.play_scorching()

    def ship_lose_life(self):
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        self.sb.prep_ships()
        if self.stats.ships_left <= 0:
            self.has_lives = False
    
    def update_shield(self):
        # If RNG Shield Colors are enabled, set the color via RNG.
        if self.settings.rng_shield_color: self.shield_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        # Else, proceed as normal:
        elif not self.settings.rng_shield_color:
            # Increment Time
            self.shield_flash_timer += self.si_game.dt
            # If enough time has passed:
            if self.shield_flash_timer >= self.shield_flash_delay:
                self.shield_flash_timer = 0
                self.shield_flash_index += 1
                self.shield_flash_index %= len(self.shield_flash_colors)
                self.shield_color = self.shield_flash_colors[self.shield_flash_index]

        self.image_shield = get_outline(self.image, color = self.shield_color, threshold = 100, alpha = 255)
        self.image_shield_rect = self.image_shield.get_rect()
        self.image_shield_rect.center = self.rect.center
        
        self.draw_shield()

    def update_ghost(self):
        # If RNG Shield Colors are enabled, set the color via RNG.
        if self.settings.rng_ghost_color: self.ghost_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        # Else, proceed as normal:
        elif not self.settings.rng_ghost_color:
            # Increment Time
            self.ghost_flash_timer += self.si_game.dt
            # If enough time has passed:
            if self.ghost_flash_timer >= self.ghost_flash_delay:
                self.ghost_flash_timer = 0
                self.ghost_flash_index += 1
                self.ghost_flash_index %= len(self.ghost_flash_colors)
                self.ghost_color = self.ghost_flash_colors[self.ghost_flash_index]
    
        self.image_ghost = get_outline(self.image, color = self.ghost_color, threshold = 100, alpha = 255)
        self.image_ghost_rect = self.image_ghost.get_rect()
        self.image_ghost_rect.center = self.rect.center
        
        if self.v != Vector(0,0):
            self.draw_ghost()

    def update(self):   
            
            # Events for once ship explosion is finished.
            if self.is_dying and self.ship_explosion_timer.finished():
                self.is_dying = False
                self.destroyed = True

                self.destruct_sound_played = False

            # If Healthy
            if not self.is_dying and not self.destroyed:
                self.x += self.v.x * self.si_game.dt
                self.y += self.v.y * self.si_game.dt
                self.bound()

                self.update_invulnerability()
                self.update_shields()

                # Modified - Separate Guns
                self.anchor_guns()

                # Modified - Fires Weapons Using restrictions
                self.modulate_weapons()
                
            elif self.is_dying:
                # Slight movement until explosion
                if self.ship_explosion_timer.index <= 30:
                    self.x += self.v.x * self.si_game.dt / 10
                    self.y += self.v.y * self.si_game.dt / 10
                    self.bound()

                # When the ship explosion begins the second half of its animation:
                if not self.destruct_sound_played and self.ship_explosion_timer.index >= 30:
                    self.si_game.sound.stop_scorching()
                    self.si_game.sound.play_ship_boom()
                    self.destruct_sound_played = True

            # Update Lasers
            self.lasers.update()

            # Draw Fighter Ghost # We are using rect before it gets updated.
            if not self.is_dying and not self.destroyed:
                self.update_ghost()

            # Prep Fighter Frame
            self.image = self.timer.current_image()
            self.rect = self.image.get_rect()
            
            # Draw Fighter
            self.draw()

            # Draw Fighter Shield
            if not self.is_dying and not self.destroyed:
                self.update_shield()

    def draw(self):
        self.rect.centerx, self.rect.centery = self.x, self.y
        self.screen.blit(self.image, self.rect)
    
    def draw_shield(self):
        self.screen.blit(self.image_shield, self.image_shield_rect)

    def draw_ghost(self):
        self.screen.blit(self.image_ghost, self.image_ghost_rect)

    def update_dynamic_settings(self):
        self.laser_speed = self.settings.laser_speed    # Dynamic
        self.laser_height = self.settings.laser_height  # Dynamic

def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
