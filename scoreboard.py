import pygame.font
from pygame.sprite import Group
from ship import Ship

from colors import*
from fonts import PIXEL

class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, si_game):
        """Initialize scorekeeping attributes."""
        self.si_game = si_game
        self.screen = si_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = si_game.settings
        self.stats = si_game.stats

        # Font settings for scoring information.
        self.text_color = WHITE
        self.font = pygame.font.Font(PIXEL, 48)

        self.prep_score_level_ships()
        self.load_high_scores()
        self.prep_high_score()

    def prep_score_level_ships(self):
        """Prepare the initial score images.""" 
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.si_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def save_high_scores(self):
        """Save the top 10 high scores to a file."""
        # Sort the list of high scores in descending order
        if self.stats.score > min(self.high_scores):
            self.high_scores.append(self.stats.score)
            self.high_scores = sorted(self.high_scores, reverse=True)[:10]  # Keep only the top 10 scores
            with open("high_scores.txt", "w") as file:
                for score in self.high_scores:
                    file.write(f"{score}\n")

    def load_high_scores(self):
        """Load the top 10 high scores from a file."""
        self.high_scores = []
        try:
            with open("high_scores.txt", "r") as file:
                self.high_scores = [int(line.strip()) for line in file.readlines()]
                self.high_scores = sorted(self.high_scores, reverse=True)[:10]  # Ensure top 10 scores
        except (ValueError, FileNotFoundError):
            for _ in range(10): self.high_scores.append(0) # Handle the case where the file is empty or corrupted

        # Set the highest score as the game's high score
        if self.high_scores:
            self.stats.high_score = self.high_scores[0]  # Top score will be the first in the list
        else:
            self.stats.high_score = 0

