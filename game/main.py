"""Game main module."""
import sys

import pygame as pg
from pytmx.util_pygame import load_pygame

from code.settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS, LAYERS
from code.tiles import Tile, CollisionTile, MovingPlatform
from code.player import Player
from code.sprites import AllSprites


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

        self.setup()

    def setup(self):
        """Sets up game."""
        tmx_map = load_pygame(PATHS['map'])

        print(tmx_map.get_layer_by_name('Level').tiles())

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
                    groups=self.all_sprites,
                    path=PATHS['player'],
                    collision_sprites=self.collision_sprites
                )

        # Platforms
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites,
                                                           self.collision_sprites, self.platform_sprites])
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
            self.all_sprites.custom_draw(player=self.player)

            pg.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
