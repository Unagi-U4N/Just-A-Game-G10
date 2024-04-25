# Some of the python files are not complete yet, to test them please comment out the parts that are undone
# Undone part used in this file: Tilemap, Clouds


import pygame, sys, random, math
from utils import *
from entities import PhysicsEntity, Player, Enemy
from tilemap import Tilemap
from clouds import Clouds
from particle import Particle
from spark import Spark

class Play():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.assets = game.assets
        self.clouds = Clouds(self.assets["clouds"], 16)
        self.player = Player(game, (100, 50), (16, 30))
        self.tilemap = Tilemap(game, tile_Size=32)
        self.daybg = scale_images(self.assets["day"],(1200, 675))

        
        # self.tilemap.load("map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 20 + tree["pos"][1], 23, 13))
        

        self.enemies = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (16, 30))) # Scaled

        # Deals with offset, when the player moves, everything moves in the opposite direction to make the illusion that the player is moving
        self.scroll = [0, 0]

        self.movements = [False, False]
        self.clock = game.clock
        self.screen = game.screen
        self.display = game.display

        if game.particles is not None:
            game.particles.clear()
        self.particles = game.particles

        if game.sparks is not None:
            game.sparks.clear()
        self.sparks = game.sparks

        if game.projectiles is not None:
            game.projectiles.clear()
        self.projectiles = game.projectiles

    def run(self):
        
        # Make sure that the player is always in the middle of the screen
        self.scroll[0] += (self.player.pos[0] - self.scroll[0] - 600) / 20
        self.scroll[1] += (self.player.pos[1] - self.scroll[1] - 337.5) / 20
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        
        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
        

        self.display.blit(self.daybg, (0, 0))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)

        self.tilemap.render(self.display, offset=render_scroll)
        
        for enemy in self.enemies.copy():
            enemy.update(self.tilemap, (0, 0))
            enemy.render(self.display, offset=render_scroll)

        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 2, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)
        
        # [[x, y], direction, timer]
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            img = self.assets["projectile"]
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            
            # When dash, invincible
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    self.projectiles.remove(projectile)
                    
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

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
        