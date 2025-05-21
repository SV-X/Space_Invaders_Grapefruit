import pygame as pg 
from point import Point 
from vector import Vector

class Image:
	def __init__(self, si_game, filename, scale=0.5, ctr=Point(), v=Vector(2, 3)): 
		self.si_game = si_game 
		self.scr_rect = self.screen.get_rect()
		self.screen = si_game.screen
		self.scale, self.ctr, self.v = scale, ctr, v
		self.img = pg.transform.rotozoom(pg.image.load(filename), 0, scale)
		self.rect = self.img.get_rect()
		self.x, self.y = ctr.x, ctr.y
	def __str__(self): return f"Image[filename={self.filename},scale={self.scale},ctr={self.ctr}]"
	def bound(self):
		self.ctr.x = max(0, min(self.ctr.x, self.scr_rect.width - self.rect.width))
		self.ctr.y = max(0, min(self.ctr.y, self.scr_rect.height - self.rect.height))
	def bounding_rect(self): return self.rect
	def update(self):
		self.ctr += self.v
		self.bound()
		self.draw()
	def draw(self): 
		self.centerx, self.centery = self.ctr.x, self.ctr.y
		self.screen.blit(self.img, self.rect)

def main(): print("Hey! Run from alien_invasion.py!")

if __name__ == '__main__':
	main() 
