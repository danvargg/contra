"""Game overlays."""
import pygame as pg

from code.settings import PATHS


class HealthBar:
    def __init__(self, player):
        self.player = player
        self.display_surface = pg.display.get_surface()
        self.health_surf = pg.image.load(PATHS['health']).convert_alpha()

    def display(self):
        for h in range(self.player.health):
            x = 10 + h * (self.health_surf.get_width() + 1)
            y = 10
            self.display_surface.blit(self.health_surf, (x, y))
