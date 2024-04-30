# Some of the python files are not complete yet, to test them please comment out the parts that are undone
# Undone part used in this file: Tilemap, Clouds


import pygame, sys, random, math, time
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
        self.screen = game.screen
        self.display = game.display
        self.assets = game.assets
        self.clouds = Clouds(self.assets["clouds"], 16)
        self.player = Player(game, (100, 50), (16, 30), 1.5)
        self.tilemap = Tilemap(game, tile_Size=32)
        self.daybg = scale_images(self.assets["day"],(1200, 675))
        self.level = 0
        self.reasonofdeath = None
        self.playedwaste = False
        self.deadmsg = ""
        self.death_msg = {
            "fall" : ["You fell to your death", "You ignored physics class", "You thought you were superman", "So this is the FALLEN angel?", "Just a reminder you're not a bird"],
            "enemy" : ["You were killed by an enemy", "Unfortunately you are not bulletproof", "You were too weak", "You were too fragile", "You thought bullet was friendly", "Stop playing, touch grass"],
        }

        self.load_level(self.level)

    def load_level(self, map_id):

        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 20 + tree["pos"][1], 23, 13))
        
        self.enemies = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (16, 30), difficulty=map_id+1)) # Scaled

        # Deals with offset, when the player moves, everything moves in the opposite direction to make the illusion that the player is moving
        self.scroll = [0, 0]
        self.dead = 0 
        self.firsthit = False
        self.deadscreen = False
        self.deadscreentrans = 0

        self.movements = [False, False]

        if self.game.particles is not None:
            self.game.particles.clear()
        self.particles = self.game.particles

        if self.game.sparks is not None:
            self.game.sparks.clear()
        self.sparks = self.game.sparks

        if self.game.projectiles is not None:
            self.game.projectiles.clear()
        self.projectiles = self.game.projectiles

        if self.game.exclamation is not None:
            self.game.exclamation.clear()
        self.exclamation = self.game.exclamation

    def run(self):
        
        # Dead screen transition
        if self.dead or self.player.airtime():
            self.deadscreen = True
            self.dead += 1
            if self.reasonofdeath is None:
                self.reasonofdeath = "fall"
                self.deadmsg = random.choice(self.death_msg[self.reasonofdeath])
            self.deadscreentrans = min(150, self.deadscreentrans + 3)
                            
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
            kill = enemy.update(self.tilemap, (0, 0))
            if int(enemy.pos[0]) in range(int(self.player.pos[0] - self.display.get_width() / 2 - 100), int(self.player.pos[0] + self.display.get_width() / 2 + 100)):
                enemy.render(self.display, offset=render_scroll)

            if kill:
                self.enemies.remove(enemy)
        
        
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 1.5, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)

        # exclamation mark above enemy heads
        for exclamation in self.exclamation.copy():
            img = self.assets['!']
            if int(exclamation[0]) in range(int(self.player.pos[0] - self.display.get_width() / 2 - 100), int(self.player.pos[0] + self.display.get_width() / 2 + 100)):
                self.display.blit(img, (exclamation[0] - img.get_width() / 2 - render_scroll[0], exclamation[1] - img.get_height() - render_scroll[1] - 20))
                self.exclamation.remove(exclamation)
        
        # [[x, y], direction, timer]
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            img = self.assets['projectile']
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            
            # Check if the projectile hits a solid tile
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random(), (255,0,0)))
            
            # Check if the projectile is out of bounds
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            
            # Check if the projectile hits the player, when the player is not dashing
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    if not self.firsthit:
                        self.dead += 1
                        if self.reasonofdeath is None:
                            self.reasonofdeath = "enemy"
                            self.deadmsg = random.choice(self.death_msg[self.reasonofdeath])
                        self.firsthit = True
                    self.projectiles.remove(projectile)
                    for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random(), (255,0,0)))
                        self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
             
        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(self.display, offset=render_scroll)
            if kill:
                self.sparks.remove(spark)

        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)
        
        # Load dead screen
        if self.deadscreen:
            self.movements = [False, False]
            if not self.playedwaste:
                self.playedwaste = True   
                # self.game.sfx['ambience'].stop()
                self.game.sfx['wasted'].play()
            img = pygame.Surface((1200, 675))
            img.fill((0,0,0))
            img.set_alpha(self.deadscreentrans)
            self.display.blit(img, (0,0))
            if self.dead > 130:
                render_text("Wasted", pygame.font.Font('freesansbold.ttf', 64), (255, 0, 0), 600, 250, self.display)
                render_text(self.deadmsg, pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), 600, 300, self.display)
                render_text("Press SPACE to restart", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), 600, 600, self.display)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.dead = 0
                            self.firsthit = False
                            self.deadscreen = False
                            self.deadmsg = ""
                            self.reasonofdeath = None
                            self.load_level(self.level)
                            self.playedwaste = False
                            # self.game.sfx['ambience'].play(-1)

        # This part will check the movements of the player
        if not self.dead:
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
            