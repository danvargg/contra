"""Game main module."""
import sys
import pygame as pg

from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Main:
    """Game main class."""

    def __init__(self):
        """Initializes game."""
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Contra')
        self.clock = pg.time.Clock()

    def run(self):
        """Game entry point."""
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.display_surface.fill((249, 131, 103))

            pg.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
