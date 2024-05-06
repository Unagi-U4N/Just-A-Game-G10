import pygame
import sys
from utils import *
from tilemap import Tilemap

# No use of render scale, we render 1:1
RENDER_SCALE = 2

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Just A Game')
        self.screen = pygame.display.set_mode((1200, 675))
        self.display = pygame.Surface((1200, 675))
        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": scale_images(load_images("tiles/decor")),
            "grass": scale_images(load_images("tiles/grass")),
            "stone": scale_images(load_images("tiles/stone")),
            "large_decor": scale_images(load_images("tiles/large_decor")),
            "spawners": scale_images(load_images("tiles/spawners")),
        }

        self.tilemap = Tilemap(self, tile_Size=32)
        self.movements = [False, False, False, False]

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.count = 0

        self.bgs = [
            scale_images(load_image("background/daybg.png"), (1200, 675)),
            scale_images(load_image("background/nightbg.png"), (1200, 675))
        ]

    def draw_tile_selector(self):
        # Draw the tile selector
        tile_selector_y = 20
        for i, tile_group in enumerate(self.tile_list):
            tile_img = self.assets[tile_group][0]  # Only use the first variant for the selector
            self.display.blit(tile_img, (20, tile_selector_y))
            if i == self.tile_group:
                pygame.draw.rect(self.display, (255, 0, 0), (18, tile_selector_y - 2, tile_img.get_width() + 4, tile_img.get_height() + 4), 2)
            tile_selector_y += tile_img.get_height() + 10

    def draw_grid(self):
        # Draw grid if needed
        if self.ongrid:
            for x in range(0, self.display.get_width(), self.tilemap.tile_size):
                pygame.draw.line(self.display, (100, 100, 100), (x, 0), (x, self.display.get_height()))
            for y in range(0, self.display.get_height(), self.tilemap.tile_size):
                pygame.draw.line(self.display, (100, 100, 100), (0, y), (self.display.get_width(), y))

    def run(self):
        while True:

            self.scroll[0] += (self.movements[1] - self.movements[0])
            self.scroll[1] += (self.movements[3] - self.movements[2])

            self.display.fill((255, 255, 255))
            self.display.blit(self.bgs[self.count], (0, 0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            self.draw_tile_selector()  # Draw tile selector
            self.draw_grid()  # Draw grid

            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile.set_alpha(200)

            mousepos = pygame.mouse.get_pos()
            tile_pos = (int((mousepos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mousepos[1] + self.scroll[1]) // self.tilemap.tile_size))
            if self.ongrid:
                self.display.blit(current_tile, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                  tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile, mousepos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group],
                                                                                    'variant': self.tile_variant,
                                                                                    'pos': tile_pos}
            if self.right_clicking:
                if str(tile_pos[0]) + ';' + str(tile_pos[1]) in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])]

                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                          tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mousepos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile, (20, 20))

            # This part will check the movements of the player
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group],
                                                                'variant': self.tile_variant,
                                                                'pos': (mousepos[0] + self.scroll[0],
                                                                        mousepos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        # Loop through the backgrounds
                        self.count += 1
                        self.count %= len(self.bgs)
                    if event.key == pygame.K_o:
                        self.tilemap.save("map.json")
                    if event.key == pygame.K_a:
                        self.movements[0] = True
                    if event.key == pygame.K_d:
                        self.movements[1] = True
                    if event.key == pygame.K_w:
                        self.movements[2] = True
                    if event.key == pygame.K_s:
                        self.movements[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movements[0] = False
                    if event.key == pygame.K_d:
                        self.movements[1] = False
                    if event.key == pygame.K_w:
                        self.movements[2] = False
                    if event.key == pygame.K_s:
                        self.movements[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()