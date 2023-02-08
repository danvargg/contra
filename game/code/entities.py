"""Game entities."""
import os
import glob
from math import sin

import pygame as pg
from pygame.math import Vector2 as vector

from code.settings import LAYERS


class Entity(pg.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)

        # graphics setup
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right'

        # image setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Level']
        self.mask = pg.mask.from_surface(self.image)

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400

        # shooting setup
        self.shoot = shoot
        self.can_shoot = True
        self.shoot_time = None
        self.cooldown = 200
        self.duck = False

        # health
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = None
        self.invul_duration = 500

    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pg.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pg.time.get_ticks()

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True

    def invul_timer(self):
        if not self.is_vulnerable:
            current_time = pg.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True

    def import_assets(self, path):
        self.animations = {}
        for subdir in os.listdir(path):
            subdir_path = os.path.join(path, subdir)
            if os.path.isdir(subdir_path):
                self.animations[subdir] = []
                for file in sorted(glob.glob(os.path.join(subdir_path, '*.png'))):
                    surf = pg.image.load(file).convert_alpha()
                    self.animations[subdir].append(surf)
