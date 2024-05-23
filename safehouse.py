import pygame, sys, random 
import utils
from tilemap import Tilemap
from clouds import Clouds
from particle import Particle


class Safehouse:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.assets = game.assets
        self.player = game.player
        self.dialogues = game.dialogues
        self.movements = [False, False]
        self.playerprofile = [self.player.name, self.player.level, self.player.gold, self.player.HP, self.player.speed]
        self.scroll = [0, 0]
        self.display = self.screen 
        self.bg = utils.scale_images(self.assets["day"],(1200, 675))
        self.clouds = Clouds(self.assets["clouds"], 16)
        self.tilemap = Tilemap(game, tile_Size=32)
        self.sfx = game.sfx
        self.particles = []
        self.load_level("safehouse")

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
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * 2, 0)) # update(self, tilemap, movement=(0,0))
        self.player.render(self.display, offset=render_scroll)
        utils.render_img(self.assets["startcontrols"], 200, 600, self.display)

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

    def load_level(self, map_id):

        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 20 + tree["pos"][1], 23, 13))
        print("Safehouse")