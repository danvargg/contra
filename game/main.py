"""Game main module."""
import sys

import pygame as pg
from pytmx.util_pygame import load_pygame

from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS, LAYERS
from code.tiles import Tile, CollisionTile, MovingPlatform
from code.player import Player
from code.sprites import AllSprites
from code.bullets import Bullet, FireAnimation
from code.enemies import Enemy
from code.overlays import HealthBar

# TODO: delete enemies folder


class Main:
    """Game main class."""

    def __init__(self):
        """Initializes game."""
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = pg.image.load(PATHS['game_icon'])
        pg.display.set_icon(self.icon)
        pg.display.set_caption('Contra')
        self.clock = pg.time.Clock()

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pg.sprite.Group()
        self.platform_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.vulnerable_sprites = pg.sprite.Group()

        self.setup()
        self.health_bar = HealthBar(self.player)

        # bullet images
        self.bullet_surf = pg.image.load(PATHS['bullet']).convert_alpha()
        self.fire_surfs = [
            pg.image.load(PATHS['fire_0']).convert_alpha(), pg.image.load(PATHS['fire_1']).convert_alpha()
        ]

    def setup(self):
        """Sets up game."""
        tmx_map = load_pygame(PATHS['map'])

        # Collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile(pos=(x * 64, y * 64), surf=surf, groups=[self.all_sprites, self.collision_sprites])

        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(pos=(x * 64, y * 64), surf=surf, groups=self.all_sprites, z=LAYERS[layer])

        # Objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.vulnerable_sprites],
                    path=PATHS['player'],
                    collision_sprites=self.collision_sprites,
                    shoot=self.shoot
                )
            if obj.name == 'Enemy':
                Enemy(
                    pos=(obj.x, obj.y),
                    path=PATHS['enemy'],
                    groups=[self.all_sprites, self.vulnerable_sprites],
                    shoot=self.shoot,
                    player=self.player,
                    collision_sprites=self.collision_sprites
                )

        # Platforms
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform(
                    (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites]
                )
            else:  # border
                border_rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:  # up
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:  # down
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collisions(self):
        # obstacles
        for obstacle in self.collision_sprites.sprites():
            pg.sprite.spritecollide(obstacle, self.bullet_sprites, True)

        # entities
        for sprite in self.vulnerable_sprites.sprites():
            if pg.sprite.spritecollide(sprite, self.bullet_sprites, True, pg.sprite.collide_mask):
                sprite.damage()

    def shoot(self, pos, direction, entity):
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

    def run(self):
        """Game entry point."""
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.display_surface.fill((249, 131, 103))

            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()
            self.all_sprites.custom_draw(player=self.player)
            self.health_bar.display()

            pg.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
