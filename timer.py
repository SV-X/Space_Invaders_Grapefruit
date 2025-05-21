import pygame
from time import time

class Timer:
    def __init__(self, images, start_index=0, loop_continuously=True, delta=1000, running=True):
        if len(images) == 0: raise ValueError("timer's list of images is empty")
        if start_index > len(images) - 1: raise ValueError("start_index out of bounds")
        self.images = images 
        self.delta = delta
        self.loop_continuously = loop_continuously
        self.index = start_index
        self.latest = pygame.time.get_ticks()
        self.running = running

    def start(self): self.running = True

    def finished(self): 
        return not self.loop_continuously and self.index == len(self.images) - 1

    def current_image(self):
        if not self.running: return self.images[self.index] 

        now = pygame.time.get_ticks()
        if now - self.latest > self.delta and not self.finished(): 
            # print(f'now: {now}, latest: {self.latest}, now - latest: {now - self.latest}, delta: {self.delta}, index: {self.index}')
            self.index += 1
            self.latest = now
        if self.loop_continuously: self.index %= len(self.images)
        return self.images[self.index]
    
    def advance_frame(self):
        self.index = (self.index + 1) % len(self.images)
        return self.images[self.index]
