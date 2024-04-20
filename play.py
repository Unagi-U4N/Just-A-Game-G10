
import pygame, sys
from utils import *
from entities import PhysicsEntity
from tilemap import Tilemap
from clouds import Clouds

class Play():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.clouds = Clouds(game.assets["clouds"], 16)
        self.player = PhysicsEntity(game, "player", (100, 50), (16, 30))
        self.tilemap = Tilemap(game, tile_Size=32)
        self.daybg = pygame.transform.scale(game.assets["day"], (1200, 675))

        # Deals with offset, when the player moves, everything moves in the opposite direction to make the illusion that the player is moving
        self.scroll = [0, 0]

        self.movements = [False, False]
        self.clock = game.clock
        self.screen = game.screen
        self.display = game.display

    def run(self):
        
        # Make sure that the player is always in the middle of the screen
        self.scroll[0] += (self.player.pos[0] - self.scroll[0] - 600) / 20
        self.scroll[1] += (self.player.pos[1] - self.scroll[1] - 337.5) / 20
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.display.fill((255, 255, 255))

        self.display.blit(self.daybg, (0, 0))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)
        self.tilemap.render(self.display, offset=render_scroll)
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 3, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)

        # This part will check the movements of the player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movements[0] = True
                if event.key == pygame.K_d:
                    self.movements[1] = True
                if event.key == pygame.K_w:
                    self.player.velocity[1] = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movements[0] = False
                if event.key == pygame.K_d:
                    self.movements[1] = False
