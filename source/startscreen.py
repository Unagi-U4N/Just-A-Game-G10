import pygame, sys, random, math
from source.utils import *
from source.entities import Player, Enemy
from source.tilemap import Tilemap
from source.clouds import Clouds
from source.particle import Particle

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.sfx = game.sfx
        self.screen = game.screen
        self.display = game.display
        self.clock = game.clock
        self.width = 1200
        self.height = 675
        self.assets = game.assets
        self.clouds = Clouds(self.assets["clouds"], 16)
        self.player = Player(game, (100, 50))
        self.tilemap = Tilemap(game, tile_Size=32)
        self.bg = self.assets["day"]
        self.cooldown = 60
        self.startcountdown = False
        self.name = ""

        self.load_level("start")

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
                enemy = Enemy(self, spawner["pos"], (16, 30), name="") # Scaled
                self.enemies.append(enemy)

        # Sort the enemies based on their position
        self.enemies.sort(key=lambda x: x.pos[0])
        for i, enemy in enumerate(self.enemies):
            if i == 1:
                enemy.name = "New Game"
            elif i == 2:
                enemy.name = "Load Game"
            elif i == 3:
                enemy.name = "Exit Game"

        self.movements = [False, False]

        self.scroll = [0, 0]

        if self.game.particles is not None:
            self.game.particles.clear()
        self.particles = self.game.particles

        if self.game.sparks is not None:
            self.game.sparks.clear()
        self.sparks = self.game.sparks

    def run(self):
        
        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
        
        # Make sure that the player is always in the middle of the screen
        self.scroll[0] += (self.player.pos[0] - self.scroll[0] - 600) / 20
        self.scroll[1] += (self.player.pos[1] - self.scroll[1] - 337.5) / 20
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.display.blit(self.bg, (0, 0))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)

        self.tilemap.render(self.display, offset=render_scroll)
        
        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0, 0), move=False)
            if int(enemy.pos[0]) in range(int(self.player.pos[0] - self.display.get_width() / 2 - 300), int(self.player.pos[0] + self.display.get_width() / 2 + 300)):
                enemy.render(self.display, offset=render_scroll)
                if enemy.name != "":
                    font1 = pygame.font.Font(self.game.font, 30)
                    font2 = pygame.font.Font(self.game.font, 40)
                    render_text(enemy.name, font1, (255, 255, 255), enemy.pos[0] - self.scroll[0], enemy.pos[1] - self.scroll[1] - 50, self.display, False)
                    if self.player.rect().colliderect(enemy.interact):
                        render_text("Press SPACE to dash", font2, (255, 255, 255), 600, 550, self.display)

            if kill:
                self.startcountdown = True
                self.name = enemy.name
                self.enemies.remove(enemy)
        
        if self.startcountdown:
            self.cooldown -= 1
        if self.cooldown <= 0:
            return self.name

        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 2, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)
        # render_img(self.assets["startcontrols"], 200, 600, self.display)
        
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
                    if self.player.jump():
                        self.sfx['jump'].play()
                if event.key == pygame.K_SPACE:
                    self.player.dash()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movements[0] = False
                if event.key == pygame.K_d:
                    self.movements[1] = False
