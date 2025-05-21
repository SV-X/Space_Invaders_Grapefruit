import pygame as pg 
import time

class Sound:
    def __init__(self):
        pg.mixer.set_num_channels(64)

        self.music_dict = {"Frost_Man" : 'sounds/music/Frost_Man.mp3',
                           "Frost_Man_v2" : 'sounds/music/Frost_Man_Stage.mp3',
                           "Game_Over" : 'sounds/music/bgm_gameover.ogg',
                           "Turbo" : 'sounds/music/Turbo Sexy Trunks - Neostorm.mp3'}
        self.music_key = "Frost_Man"

        pg.mixer.music.load(self.music_dict[self.music_key])
        pg.mixer.music.set_volume(0.5)

        self.music_playing = False

        # Game Over
        self.gameover = pg.mixer.Sound('sounds/event/voc_a_gameover.wav')
        self.gameover.set_volume(0.5)

        # Booms
        self.boom_volume = 0.2

        self.ship_boom = pg.mixer.Sound('sounds/sfx/boom_big.wav')
        self.ship_boom.set_volume(self.boom_volume)

        self.alien_boom = pg.mixer.Sound('sounds/sfx/sfx_bonus.wav')
        self.alien_boom.set_volume(self.boom_volume)

        # Bang
        self.ship_hit = pg.mixer.Sound('sounds/sfx/bang_a.wav')
        self.ship_hit.set_volume(self.boom_volume)

        # Lasers
        self.laser_volume = 0.1

        self.laser_fire_a = pg.mixer.Sound('sounds/sfx/laser_a.wav')
        self.laser_fire_a.set_volume(self.laser_volume)

        self.laser_fire_b = pg.mixer.Sound('sounds/sfx/laser_b.wav')
        self.laser_fire_b.set_volume(self.laser_volume)

        self.laser_fire_c = pg.mixer.Sound('sounds/sfx/laser_c.wav')
        self.laser_fire_c.set_volume(self.laser_volume)

        self.laser_fire_d = pg.mixer.Sound('sounds/sfx/laser_d.wav')
        self.laser_fire_d.set_volume(self.laser_volume)

        # Lock-on
        self.lockon = pg.mixer.Sound('sounds/sfx/sfx_lockon.wav')
        self.lockon.set_volume(self.boom_volume)

        # Scorching
        self.scorching = pg.mixer.Sound('sounds/sfx/sfx_scorching.wav')
        self.scorching.set_volume(self.boom_volume)

        # One Up
        self.one_up = pg.mixer.Sound('sounds/sfx/sfx_oneup.wav')
        self.one_up.set_volume(self.boom_volume)

    def play_background(self): 
        pg.mixer.music.play(-1, 0.0)
        self.music_playing = True
    
    def load_game_bgm(self):
        self.music_key = "Frost_Man"
        pg.mixer.music.load(self.music_dict[self.music_key])

    def load_game_bgm_v2(self):
        self.music_key = "Frost_Man_v2"
        pg.mixer.music.load(self.music_dict[self.music_key])

    def load_gameover_bgm(self):
        self.music_key = "Game_Over"
        pg.mixer.music.load(self.music_dict[self.music_key])
    
    def load_turbo_bgm(self):
        self.music_key = "Turbo"
        pg.mixer.music.load(self.music_dict[self.music_key])

    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(1.5)       # sleep until game over sound has finished

    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False 

    def play_ship_boom(self):
        self.ship_boom.play()

    def play_alien_boom(self):
        self.alien_boom.play()

    def play_ship_hit(self):
        self.ship_hit.play()

    def play_laser_fire_a(self):
        self.laser_fire_a.play()

    def play_laser_fire_b(self):
        self.laser_fire_b.play()

    def play_laser_fire_c(self):
        self.laser_fire_c.play()

    def play_laser_fire_d(self):
        self.laser_fire_d.play()

    def play_scorching(self):
        self.scorching.play(loops=-1)
    
    def stop_scorching(self):
        self.scorching.stop()

    def play_lockon(self):
        self.lockon.play(loops=-1)
    
    def stop_lockon(self):
        self.lockon.stop()

    def play_one_up(self):
        self.one_up.play()