import pygame
import sys
from utils import *
from tilemap import Tilemap

# Constants
SCREEN_SIZE = (1200, 675)
RENDER_SCALE = 2
TILE_SELECTOR_WIDTH = 150
TILE_SIZE = 32

class Editor:
    def __init__(self):
        try:
            pygame.init()
        except pygame.error as e:
            print("Pygame initialization failed:", e)
            sys.exit()

        pygame.display.set_caption('Just A Game')
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.display = pygame.Surface(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.paused =True
        self.paused_img = scale_images(load_image("editor_pause.png"), (1200, 675))

        self.assets = {
            "decor": scale_images(load_images("tiles/decor")),
            "grass": scale_images(load_images("tiles/grass")),
            "stone": scale_images(load_images("tiles/stone")),
            "metal": scale_images(load_images("tiles/metal")),
            "large_decor": scale_images(load_images("tiles/large_decor")),
            "spawners": scale_images(load_images("tiles/spawners")),
            "tile_background": scale_images(load_images("tiles/background")),
        }

        self.tilemap = Tilemap(self, tile_Size=TILE_SIZE)
        self.movements = [False, False, False, False]

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass


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
            scale_images(load_image("background/daybg.png"), SCREEN_SIZE),
            scale_images(load_image("background/nightbg.png"), SCREEN_SIZE)
        ]

        self.tile_selector_rects = []

    def draw_tile_selector(self):
        # Draw the tile selector
        tile_selector_y = 20
        for i, tile_group in enumerate(self.tile_list):
            tile_img = self.assets[tile_group][0]  # Only use the first variant for the selector
            self.display.blit(tile_img, (SCREEN_SIZE[0] - TILE_SELECTOR_WIDTH + 20, tile_selector_y))
            if i == self.tile_group:
                pygame.draw.rect(self.display, (255, 0, 0), (SCREEN_SIZE[0] - TILE_SELECTOR_WIDTH + 18, tile_selector_y - 2, tile_img.get_width() + 4, tile_img.get_height() + 4), 2)
            self.tile_selector_rects.append(pygame.Rect(SCREEN_SIZE[0] - TILE_SELECTOR_WIDTH, tile_selector_y, tile_img.get_width(), tile_img.get_height()))
            tile_selector_y += tile_img.get_height() + 10

        # Display current tile variant
        font = pygame.font.Font(None, 24)
        variant_text = font.render(f"Variant: {self.tile_variant}", True, (0, 0, 0))
        self.display.blit(variant_text, (SCREEN_SIZE[0] - TILE_SELECTOR_WIDTH + 20, SCREEN_SIZE[1] - 50))

    def draw_grid(self):
        # Draw grid if needed
        if self.ongrid:
            for x in range(0, SCREEN_SIZE[0], self.tilemap.tile_size):
                pygame.draw.line(self.display, (100, 100, 100), (x, 0), (x, SCREEN_SIZE[1]))
            for y in range(0, SCREEN_SIZE[1], self.tilemap.tile_size):
                pygame.draw.line(self.display, (100, 100, 100), (0, y), (SCREEN_SIZE[0], y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                    if not self.ongrid:
                        mousepos = pygame.mouse.get_pos()
                        self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group],
                                                            'variant': self.tile_variant,
                                                            'pos': (mousepos[0] + self.scroll[0],
                                                                    mousepos[1] + self.scroll[1])})
                elif event.button == 3:
                    self.right_clicking = True
                elif self.shift and event.button in (4, 5):
                    # Scroll through variants with shift + mouse wheel
                    self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]]) \
                        if event.button == 4 else (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                elif event.button in (4, 5):
                    # Change tile group with mouse wheel
                    self.tile_group = (self.tile_group - 1) % len(self.tile_list) if event.button == 4 \
                        else (self.tile_group + 1) % len(self.tile_list)
                    self.tile_variant = 0  # Reset variant to 0 when changing group
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                elif event.button == 3:
                    self.right_clicking = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Loop through the backgrounds
                    self.count = (self.count + 1) % len(self.bgs)
                elif event.key == pygame.K_o:
                    self.tilemap.save("map.json")
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_a:
                    self.movements[0] = True
                elif event.key == pygame.K_d:
                    self.movements[1] = True
                elif event.key == pygame.K_w:
                    self.movements[2] = True
                elif event.key == pygame.K_s:
                    self.movements[3] = True
                elif event.key == pygame.K_g:
                    self.ongrid = not self.ongrid
                elif event.key == pygame.K_LSHIFT:
                    self.shift = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movements[0] = False
                elif event.key == pygame.K_d:
                    self.movements[1] = False
                elif event.key == pygame.K_w:
                    self.movements[2] = False
                elif event.key == pygame.K_s:
                    self.movements[3] = False
                elif event.key == pygame.K_LSHIFT:
                    self.shift = False

    def update_scroll(self):
        self.scroll[0] += (self.movements[1] - self.movements[0])
        self.scroll[1] += (self.movements[3] - self.movements[2])

    def render(self):
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

    def run(self):
        while True:
            self.handle_events()
            self.update_scroll()
            self.render()

            if self.paused:
                img=pygame.Surface((1200, 675))
                img.fill((0,0,0))
                img.set_alpha(150)
                self.display.blit(img, (0,0))
                render_img(self.paused_img, 0, 0, self.display, centered=False)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = not self.paused

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Editor().run()
