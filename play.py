# Some of the python files are not complete yet, to test them please comment out the parts that are undone
# Undone part used in this file: Tilemap, Clouds


import pygame, sys, random, math
from utils import *
from entities import PhysicsEntity, Player
from tilemap import Tilemap
from clouds import Clouds
# from particle import Particle

class Play():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.clouds = Clouds(game.assets["clouds"], 16)
        self.player = Player(game, (100, 50), (16, 30))
        self.tilemap = Tilemap(game, tile_Size=32)
        self.daybg = scale_images(game.assets["day"],(1200, 675))

        """
        self.tilemap.load("map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13))
        """

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

        """
        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
        """

        self.display.fill((255, 255, 255))

        self.display.blit(self.daybg, (0, 0))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)
        self.tilemap.render(self.display, offset=render_scroll)
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 3, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)

        """
        for particle in self.game.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.game.particles.remove(particle)
        """

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
                    self.player.jump()
                if event.key == pygame.K_SPACE:
                    self.player.dash()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movements[0] = False
                if event.key == pygame.K_d:
                    self.movements[1] = False
