
import pygame, sys
from utils import *
from entities import PhysicsEntity
from tilemap import Tilemap

class Play():
    def __init__(self, game):
        pygame.init()

        self.player = PhysicsEntity(game, "player", (100, 50), (16, 30))
        self.tilemap = Tilemap(game, tile_Size=32)

        self.movements = [False, False]
        self.clock = game.clock
        self.screen = game.screen
        self.display = game.display

    def run(self):

        self.display.fill((255, 255, 255))
        self.tilemap.render(self.display)
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 3, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display)

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
