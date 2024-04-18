import pygame, sys
from utils import *
from entities import PhysicsEntity

class Play():
    def __init__(self, game):
        pygame.init()
        self.player = PhysicsEntity(game, "player", (50, 50), (8, 15))
        self.movements = [False, False]
        self.clock = game.clock
        self.screen = game.screen
        self.display = game.display

    def run(self):
        self.player.update((self.movements[1] - self.movements[0], 0))
        self.player.render(self.display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movements[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movements[1] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movements[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movements[1] = False
