import pygame as pg
from pygame.sprite import Sprite, Group

BARRIER_ARCH_HEIGHT = 6
BARRIER_ARCH_WIDTH_2 = 5


class BarrierPiece(Sprite):
    health_colors = {
        6: pg.Color(0, 255, 0),
        5: pg.Color(0, 128, 255),
        4: pg.Color(0, 0, 255),
        3: pg.Color(255, 255, 0),
        2: pg.Color(255, 128, 0),
        1: pg.Color(255, 0, 0),
        0: pg.Color(0, 0, 0)
    }

    def __init__(self, si_game, pos, size):
        super().__init__()
        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        self.health = len(BarrierPiece.health_colors) - 1

        self.image = pg.Surface(size)
        self.image.fill(BarrierPiece.health_colors[self.health])
        self.rect = self.image.get_rect(topleft=pos)

    def hit(self):
        if self.settings.debug_barrier:
            print('BarrierPiece hit!')

        if self.health > 0:
            self.health -= 1
            self.image.fill(BarrierPiece.health_colors[self.health])
        if self.health == 0:
            self.kill()

    def update(self):
        pass  # Future expansion


class Barrier(Sprite):
    def __init__(self, si_game, size, piece_size, position):
        super().__init__()
        self.si_game = si_game
        self.screen = si_game.screen
        self.settings = si_game.settings
        self.piece_size = piece_size
        self.barrier_pieces = Group()

        # Create all barrier pieces
        self.create_barrier_pieces(size, position)

        # Generate a surface to represent the barrier's "container"
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

    def create_barrier_pieces(self, size, position):
        barrier_width, barrier_height = size
        piece_width, piece_height = self.piece_size

        cols = barrier_width // piece_width
        rows = barrier_height // piece_height

        for row in range(rows):
            for col in range(cols):
                # Position relative to barrier position
                x = position[0] + col * piece_width
                y = position[1] + row * piece_height

                # Skip center arch cutout
                if rows - row < BARRIER_ARCH_HEIGHT and abs(col - cols // 2) < BARRIER_ARCH_WIDTH_2:
                    continue

                piece = BarrierPiece(self.si_game, (x, y), self.piece_size)
                self.barrier_pieces.add(piece)

    def reset(self):
        self.barrier_pieces.empty()
        self.create_barrier_pieces(self.rect.size, self.rect.topleft)

    def update(self):
        # Ship lasers affect barriers
        collisions = pg.sprite.groupcollide(self.barrier_pieces, self.si_game.ship.lasers, False, True)
        for piece in collisions:
            piece.hit()

        # Alien lasers affect barriers
        for alien in self.si_game.fleet.aliens:
            collisions = pg.sprite.groupcollide(self.barrier_pieces, alien.lasers, False, True)
            for piece in collisions:
                piece.hit()

        self.barrier_pieces.update()

    def draw(self):
        self.barrier_pieces.draw(self.screen)


class Barriers:
    def __init__(self, si_game):
        self.si_game = si_game
        self.settings = si_game.settings
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):
        screen_width = self.settings.scr_width
        screen_height = self.settings.scr_height

        # Scale barrier size based on screen resolution
        base_width, base_height = 225, 120
        scale_x = screen_width / self.settings.scr_width
        scale_y = screen_height / self.settings.scr_height

        barrier_size = (int(base_width * scale_x), int(base_height * scale_y))
        piece_size = (int(10 * scale_x), int(10 * scale_y))

        top = int(screen_height * 0.70)
        spacing = (screen_width - 4 * barrier_size[0]) // 5

        positions = [
            (spacing + i * (barrier_size[0] + spacing), top)
            for i in range(4)
        ]

        for pos in positions:
            barrier = Barrier(self.si_game, barrier_size, piece_size, pos)
            self.barriers.add(barrier)

    def reset(self):
        for barrier in self.barriers:
            barrier.reset()

    def update(self):
        for barrier in self.barriers:
            barrier.update()
        
        self.draw()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()
