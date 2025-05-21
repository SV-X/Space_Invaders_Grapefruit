import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 

from alien import Alien
from ufo import UFO
from pygame.sprite import Sprite
from random import randint, choice
from collections import defaultdict

# from random import randint

class Fleet(Sprite):
    def __init__(self, si_game): 
        self.si_game = si_game
        self.screen = si_game.screen
        self.ship = si_game.ship
        self.aliens = pg.sprite.Group()
        self.settings = si_game.settings
        self.stats = si_game.stats
        self.sb = si_game.sb
        self.sound = si_game.sound
        
        self.v = Vector(self.settings.alien_speed, 0)
        # alien = Alien(si_game=si_game)
        # self.aliens.add(alien)
        self.spacing = 1.5
        self.create_fleet()

        self.lasers = pg.sprite.Group()

        # Fleet Fire
        self.fleet_fire = True
        self.fleet_rate_of_fire = self.settings.fleet_rate_of_fire
        if self.fleet_rate_of_fire == 0: self.fleet_fire = False
        else: self.fleet_fire_interval = 1.0 / self.fleet_rate_of_fire
        self.fleet_fire_accumulator = 0.0
        self.fleet_fire_ready = True

        # Speed Modifier
        self.fleet_speed_modifier = 1.0
        self.initial_fleet_count = 0
        self.current_fleet_count = 0

        # UFO
        self.ufo_active = False
        self.ufo_min_time = self.settings.ufo_min_time
        self.ufo_max_time = self.settings.ufo_max_time
        self.ufo_spawn_interval = randint(self.ufo_min_time, self.ufo_max_time) # Seconds
        self.ufo_spawn_timer = self.ufo_spawn_interval

    def initialize_fleet(self):
        self.update_dynamic_settings()
        self.reset_fleet()

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        """Create a fleet of aliens with a fixed number of columns."""
        # Set the desired number of columns and rows
        num_columns = self.settings.alien_columns
        num_rows = self.settings.alien_rows

        # Get the size of the largest alien sprite for spacing
        alien_tile = Alien.alien_tile
        tile_width = alien_tile.width * self.settings.alien_true_scale
        tile_height = alien_tile.height * self.settings.alien_true_scale

        # Calculate horizontal spacing
        column_spacing = tile_width * self.spacing
        row_spacing = tile_height * self.spacing

        # Alien Type
        alien_type = 0
        frame_index = 0
        rand_type = False

        # Edges
        self.edge_lock = False

        # Create the fleet using specified columns and calculated rows
        for row in range(int(num_rows)):
            y = (row + 1) * row_spacing + row_spacing
            
            # Specify Aliens Used For Each Row
            if row == 0:
                alien_type = 0
            elif row == 1 or row == 2:
                alien_type = 1
            elif row == 3 or row == 4:
                alien_type = 2
            else:
                rand_type = True

            for col in range(num_columns):
                if rand_type: alien_type = randint(0,2) # Random each alien
                
                x = (col + 1) * column_spacing
                new_alien = Alien(si_game = self.si_game, v=Vector(self.v.x, self.v.y), type = alien_type, animation_start = frame_index, lockstep = True)
                
                new_alien.y = y
                new_alien.rect.centery = y
                new_alien.x = x
                new_alien.rect.centerx = x
                
                self.aliens.add(new_alien)
                frame_index = (frame_index + 1) % 2
        
        # For speedup, we keep track of total initial aliens in fleet.
        self.initial_fleet_count = self.current_fleet_count = len(self.aliens)

        self.ufo_active = False

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges() and alien.is_active and alien.type == "Alien": 
                return True 
        return False
    
    def manage_fleet_direction(self):
        # Check if an alien has hit the edge
        if not self.edge_lock and self.check_edges():
            self.edge_lock = True
            self.v.x *= -1 
            for alien in self.aliens:
                if alien.is_active and alien.type == "Alien":
                    alien.v.x = self.v.x
                    alien.y += self.settings.fleet_drop_distance
                    
        # Release the edge lock once all aliens are inside bounds again
        if self.edge_lock and not self.check_edges():
            self.edge_lock = False

    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                return True
        return False
    
    def modulate_fleet_fire(self):

        if self.fleet_rate_of_fire == 0: self.fleet_fire = False
        else: self.fleet_fire_interval = 1 / (self.fleet_rate_of_fire * self.fleet_speed_modifier)

        # RoF and Firing Logic
        if self.fleet_fire: # If fleet is set to fire.
            if self.fleet_fire_ready:
                self.random_fleet_fire()
                self.fleet_fire_ready = False
                self.fleet_fire_accumulator = 0.0  # Reset accumulator on first shot
            else:
                self.fleet_fire_accumulator += self.si_game.dt
                while self.fleet_fire_accumulator >= self.fleet_fire_interval:
                    self.random_fleet_fire()
                    self.fleet_fire_accumulator -= self.fleet_fire_interval
        else:   # To progress cooldown without shooting
            # If the cooldown is active, progress the timer.
            if (not self.fleet_fire_ready) and not (self.fleet_fire_accumulator >= self.fleet_fire_interval):
                self.fleet_fire_accumulator += self.si_game.dt
            # If enough time has passed, re-enable first shot, reset timer.
            if (not self.fleet_fire_ready) and (self.fleet_fire_accumulator >= self.fleet_fire_interval):
                self.fleet_fire_ready = True
                self.fleet_fire_accumulator = 0

    def random_fleet_fire(self):
        # Checking if the list is not empty
            if self.aliens:
                # Group aliens by centerx position
                columns = defaultdict(list)
                for alien in self.aliens:
                    if alien.is_active and alien.type == "Alien": columns[alien.rect.centerx].append(alien)

                # Find the bottom alien (max centery) in each column
                bottom_aliens = [max(column, key=lambda alien: alien.rect.centery) for column in columns.values()]

                # We have to make this check, since there might not be any if remaining aliens are dying/inactive.
                if bottom_aliens:
                    # Pick a random bottom alien to fire
                    firing_alien = choice(bottom_aliens)
                    firing_alien.firing = True
                    firing_alien.modulate_weapons()
                    firing_alien.firing = False

    def manage_fleet_speed(self):
        initial_speed = 1.0
        max_speed = self.settings.fleet_max_speed

        # Current and total alien count
        total_aliens = self.initial_fleet_count
        self.current_fleet_count = len([alien for alien in self.aliens if alien.is_active and alien.type == "Alien"]) # Only counting active aliens

        # Calculate progress
        if total_aliens > 0:
            percent_remaining = self.current_fleet_count / total_aliens
            self.fleet_speed_modifier = initial_speed + ((1 - percent_remaining) ** 2) * (max_speed - initial_speed)
        else:
            self.fleet_speed_modifier = max_speed  # Safety: max speed if no aliens
    
    def update_fleet_speed(self):
        # Update Modifier
        self.manage_fleet_speed()
        # Apply Modifier
        for alien in self.aliens:
            if alien.is_active: alien.di_modifier = self.fleet_speed_modifier

    def create_UFO(self):
        if not self.ufo_active:

            if (self.ufo_spawn_timer <= 0):
                new_ufo = UFO(si_game = self.si_game, v=Vector(0, 0), type = 3)


                new_ufo.y = new_ufo.rect.height * 3
                new_ufo.rect.centery = new_ufo.y
                
                choice = randint(0,1)
                if choice == 0:
                    new_ufo.x = new_ufo.rect.width * 2 + self.settings.scr_width
                    new_ufo.rect.centerx = new_ufo.x
                    new_ufo.v.x = -abs(self.v.x * 3)

                elif choice == 1:
                    new_ufo.x = new_ufo.rect.width * -2
                    new_ufo.rect.centerx = new_ufo.x
                    new_ufo.v.x = abs(self.v.x * 3)

                self.aliens.add(new_ufo)

                # Now set the timers and flags
                self.ufo_active = True
                self.ufo_spawn_interval = randint(self.ufo_min_time, self.ufo_max_time)
                self.ufo_spawn_timer = self.ufo_spawn_interval
            
            elif (self.ufo_spawn_timer > 0):
                self.ufo_spawn_timer -= self.si_game.dt
                if self.settings.debug_UFO: print("Time Delay", self.ufo_spawn_interval)
                if self.settings.debug_UFO: print("Time Remaining", self.ufo_spawn_timer)

    def update_collisions(self):
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, False, False)

        # Check Ship Laser Collisions Against Aliens
        if collisions:
            for lasers, aliens in collisions.items():
                # self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    if alien.is_active:
                        if self.settings.debug_fleet: print(f"Laser {id(lasers)} hit alien {id(alien)} at ({alien.rect.x}, {alien.rect.y})")
                        lasers.kill()
                    alien.hit()

            # Scoring
            for alien in self.aliens:
                if (not alien.is_active and not alien.score_counted):
                    alien.score_counted = True
                    if alien.type == "Alien": self.stats.score += int(alien.points * self.settings.alien_points_multiplier)
                    elif alien.type == "UFO":
                        self.stats.score += int(alien.points * self.settings.alien_points_multiplier)
                        self.ship.adjust_max_shield(amount = 1)

            self.sb.prep_score()
            self.sb.check_high_score()
        
        # Check if aliens hit the ship. - Exploding Aliens don't affect it
        if pg.sprite.spritecollideany(self.ship, self.aliens) and not self.ship.destroyed:
            if self.settings.debug_fleet: print("Ship hit!")
            if(pg.sprite.spritecollideany(self.ship, self.aliens)).is_active == True:
                self.ship.ship_hit()

        # Check if alien lasers hit the ship
        for self.alien in self.aliens:
            if pg.sprite.spritecollideany(self.ship, self.alien.lasers) and not self.ship.destroyed:
                if self.settings.debug_fleet: print("Ship hit!")
                self.ship.ship_hit()

    def update_level(self):
        # If there are no Aliens remaining, refresh and empower.
        if not self.aliens:
            self.ship.lasers.empty()

            self.fleet_speed_modifier = 1.0

            if self.settings.increase_dynamic_speed:
                self.settings.increase_speed()
                self.update_dynamic_settings()
                self.ship.update_dynamic_settings()
            
            self.create_fleet()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            return
        
    def update(self): 
        
        # Check if aliens reached the bottom
        if self.check_bottom():
            return
        
        self.manage_fleet_direction()

        self.create_UFO()

        for alien in self.aliens:
            alien.update()

        self.modulate_fleet_fire()

        self.update_collisions()

        self.update_fleet_speed()

        self.update_level()

    # def draw(self): pass
    #     # for alien in self.aliens:
    #     #     alien.draw()

    def update_dynamic_settings(self):
        self.v = Vector(self.settings.alien_speed, 0)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
