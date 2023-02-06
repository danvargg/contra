"""Player TBD."""
import os

import pygame as pg
from pygame.math import Vector2 as vector

from code.settings import LAYERS, PATHS


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, path) -> None:
        super().__init__(groups)

        self.import_assets(path)

        self.frame_index = 0
        self.status = 'right'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Level']

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400

    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(os.walk(path)):  # TODO: refactor this
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):  # TODO: can inputs be refactored?
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, dt: float):
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def update(self, dt: float):
        self.input()
        self.move(dt=dt)
        self.animate(dt=dt)
