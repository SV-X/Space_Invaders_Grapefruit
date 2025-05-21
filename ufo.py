from alien import *
from colors import *
from fonts import *

class UFO(Alien):
    def __init__(self, si_game, v, type=3, animation_start=0, lockstep=False):
        # Initialize the UFO, using Alien's attributes but overriding some.
        super().__init__(si_game, v, type=3)
        
        # Sound Flags
        self.oscillating = False

        # Flags for tracking edge passes
        self.passed_left_edge = False
        self.passed_right_edge = False

        # Scoring
        self.pointsTrue = [50, 100, 150, 200, 300]
        self.show_score = False
        self.score_delay = 3
        self.score_timer = self.score_delay
        self.score_color = ([BLACK])

        # Color Manager
        # Highscore Text Attributes
        self.score_colors_Hyper = self.settings.shield_colors["HYPER"]["Shield"]
        self.score_colors_Strong = self.settings.shield_colors["Strong"]["Shield"]
        self.score_colors_Medium = self.settings.shield_colors["Medium"]["Shield"]
        self.score_colors_Weak = self.settings.shield_colors["Weak"]["Shield"]
        self.score_colors_Gone = self.settings.shield_colors["GONE"]["Shield"]
        self.score_text_rate = 10
        self.score_text_delay = 1.0 / self.score_text_rate
        self.score_text_timer = 0
        self.score_text_index = 0

    def hit(self):
        if not self.is_dying:
            if self.settings.debug_alien: print('ALIEN HIT! Alien is dying')
            self.is_dying = True
            self.is_active = False
            if self.oscillating:
                self.si_game.sound.stop_lockon()
                self.oscillating = False
            self.timer = self.alien_explosion_timer
            self.timer.start()

            # Extracting score
            point_index = randint(0, len(self.pointsTrue) - 1)
            self.points = self.pointsTrue[point_index]
            self.score_colors = {50: self.score_colors_Gone,
                                100: self.score_colors_Weak,
                                150: self.score_colors_Medium,
                                200: self.score_colors_Strong,
                                300: self.score_colors_Hyper}.get(self.points, [GREEN, ORANGE])
            
            self.score_color = self.score_colors[self.score_text_index]

            self.points = int(self.points * self.settings.alien_points_multiplier)

    def manage_colors(self):
        self.score_text_timer += self.si_game.dt
        # If enough time has passed:
        if self.score_text_timer >= self.score_text_delay:
            self.score_text_timer = 0
            self.score_text_index += 1
            self.score_text_index %= len(self.score_colors)
            self.score_color = self.score_colors[self.score_text_index]

    def update(self):
        if self.is_dead:
            return
        if self.is_dying and self.alien_explosion_timer.finished():
            # Once dead, show score
            if (self.score_timer >= 0):
                pass
            else:
                # Then proceed
                self.is_dying = False
                self.is_dead = True
                self.destruct_sound_played = False
                if self.settings.debug_UFO: print('UFO is dead')
                self.si_game.fleet.ufo_active = False
                self.kill()
                return
            
        if not self.oscillating and self.v.magnitude() > 0 and self.is_active:
            self.si_game.sound.play_lockon()
            self.oscillating = True
        elif self.oscillating and self.v.magnitude() <= 0:
            self.si_game.sound.stop_lockon()
            self.oscillating = False

        # Check if UFO has passed the left edge
        if not self.passed_left_edge and self.x <= 0 - self.rect.width:
            self.passed_left_edge = True
            if self.settings.debug_UFO: print("UFO has passed the left edge.")
        
        # Check if UFO has passed the right edge
        if not self.passed_right_edge and self.x >= self.settings.scr_width + self.rect.width:
            self.passed_right_edge = True
            if self.settings.debug_UFO: print("UFO has passed the right edge.")

        # If both edges have been passed, despawn the UFO
        if self.passed_left_edge and self.passed_right_edge:
            if self.settings.debug_UFO: print("UFO has passed both edges and will despawn.")
            self.si_game.fleet.ufo_active = False
            if self.oscillating:
                self.si_game.sound.stop_lockon()
                self.oscillating = False
                self.is_active = False
            self.kill()

        # Update UFO's movement
        if self.is_active:
            if not self.lockstep:
                self.x += self.v.x * self.si_game.dt * self.di_modifier
                self.y += self.v.y * self.si_game.dt * self.di_modifier
            elif self.lockstep:
                self.lockstep_move()

            # Update gun location and modulate weapons as before
            self.anchor_guns()
            self.modulate_weapons()

        elif not self.is_active:
            # if self.alien_explosion_timer.index <= 4: # I like the movement
            if not self.lockstep:
                self.x += self.v.x * self.si_game.dt / 10
                self.y += self.v.y * self.si_game.dt / 10
            elif self.lockstep:
                self.lockstep_move()
            
            if not self.destruct_sound_played and self.alien_explosion_timer.index >= 4:
                    self.si_game.sound.play_alien_boom()
                    self.destruct_sound_played = True
            
            if not self.show_score and self.alien_explosion_timer.index >= 5:
                self.show_score = True
                self.si_game.sound.play_one_up()
        
        # Continue with the normal update process as needed
        self.lasers.update()
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()
        self.draw()

    def draw(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.screen.blit(self.image, self.rect)

        if self.show_score:
            self.manage_colors()
            font = pg.font.Font(PIXEL, 40)
            score_image = font.render(f"{self.points}", True, self.score_color)
            score_rect = score_image.get_rect(center=self.rect.center)
            self.si_game.screen.blit(score_image, score_rect)
            self.score_timer -= self.si_game.dt
