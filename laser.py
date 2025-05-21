import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from random import randint

class Laser(Sprite):
    @staticmethod
    def random_color(): 
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    def __init__(self, si_game, color = (0,255,0), gun = (100, 100), v=Vector(0,1), height = 5, width = 5):
        super().__init__()
        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        self.color = color
        self.height = height
        self.width = width
        self.gun = gun
        self.rect = pg.Rect(0, 0, width, height)

        self.first_frame = True
        # self.color = self.settings.laser_color
        # self.rect.center = gun
        # self.rect.midtop = si_game.ship.rect.midtop -> Replaced
        # self.y = float(self.rect.centery)
        # self.x = float(self.rect.centerx)
        
        # Initalizing Vector
        self.v = v
        
        if self.v.y > 0:    self.rect.midbottom = gun
        elif self.v.y < 0:  self.rect.midtop = gun
        else:               self.rect.center = gun
        
        self.y = float(self.rect.centery)
        self.x = float(self.rect.centerx)

        # Continuous RNG Laser Toggle
        self.continuous_rng_laser = self.settings.continuous_rng_laser_color

    # def hit(self):
    #     laser_hit = True
    #     self.kill()

    def update(self):

        if self.first_frame:
            self.first_frame = False
        elif not self.first_frame:
            self.y -= self.v.y * self.settings.laser_speed * self.si_game.dt
            self.rect.centery = self.y

            self.x += self.v.x * self.settings.laser_speed * self.si_game.dt
            self.rect.centerx = self.x

        self.check_bounds()

        if self.continuous_rng_laser: self.color = Laser.random_color()

        self.draw()
        # # Additional Lasers
        # self.y1 -= self.settings.laser_speed
        # self.rect1.y = self.y1

        # self.y2 -= self.settings.laser_speed
        # self.rect2.y = self.y2
    
    def check_bounds(self):
        if (self.rect.bottom <= 0 or
            self.rect.top >= self.settings.scr_height
            or self.rect.left >= self.settings.scr_width
            or self.rect.right <= 0):
            self.kill()

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
