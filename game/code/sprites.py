"""Game ssprites."""
import pygame as pg
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame

from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS


class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = vector()

        # import
        self.fg_sky = pg.image.load(PATHS['fg_sky']).convert_alpha()
        self.bg_sky = pg.image.load(PATHS['bg_sky']).convert_alpha()
        tmx_map = load_pygame(PATHS['map'])

        # dimensions
        self.padding = WINDOW_WIDTH / 2
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)

    def custom_draw(self, player):

        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for x in range(self.sky_num):
            # exercise: place all of the skies in the display surface
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 850 - self.offset.y / 2.5))
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 850 - self.offset.y / 2))

        # blit all sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
