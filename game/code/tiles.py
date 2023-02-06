"""TBD."""
import pygame as pg


class Tile(pg.sprite.Sprite):
    """TBD."""

    def __init__(self, pos, surf, groups, z):
        """TBD."""
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
