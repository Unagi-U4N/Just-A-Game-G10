import pygame

NEIGHBOURS_OFFSETS = [(-1, -1), (-1, 0), (-1,1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
PHYSICS_TILES = {"stone", "grass"}

class Tilemap:
    # Create a tilemap with a grid of tiles size 16x16 (default)
    def __init__(self, game, tile_Size=16):
        self.game = game
        self.tile_size = tile_Size
        self.tilemap = {}
        self.offgrid_tiles = []

        # Generate a 10 grid of grass tiles, and a 10 grid of stone tiles for example
        for i in range (10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos):
        tiles = []
        # Get the location of the tile in the grid based on the position of the player
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOURS_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rect_around(self, pos):
        rect = []
        # If the tile is a physics tile, add rect to it
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rect.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
        return rect

    def render(self, display, offset=(0, 0)):

        # # For all of the offgrid objects that are visible on the screen, render them
        # # Tiles that are rendered off the grid, visible but unable to interact
        # for x in range(offset[0], offset[0] + display.get_width()):
        #     for y in range(offset[1], offset[1] + display.get_height()):
        #         tile_loc = str(x) + ';' + str(y)
        #         if tile_loc in self.offgrid_tiles:
        #             tile_type = tile['type']
        #             tile_variant = tile['variant']
        #             tile_pos = tile['pos']
        #             display_tile = self.game.assets[tile_type][tile_variant]
        #             display_tile = pygame.transform.scale(display_tile, (self.tile_size, self.tile_size))

        #             display.blit(display_tile, (tile_pos[0]-offset[0], tile_pos[1]-offset[1]))

        for tile in self.offgrid_tiles:
            tile_type = tile['type']
            tile_variant = tile['variant']
            tile_pos = tile['pos']
            display_tile = self.game.assets[tile_type][tile_variant]
            display_tile = pygame.transform.scale(display_tile, (self.tile_size, self.tile_size))

            display.blit(display_tile, (tile_pos[0]-offset[0], tile_pos[1]-offset[1]))
            
        # For all of the tiles that are visible on the screen, render them
        # Tiles that are rendered on the grid, visible and interactable
        for x in range(offset[0] // self.tile_size, (offset[0] + display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + display.get_height()) // self.tile_size + 1):
                tile_loc = str(x) + ';' + str(y)
                if tile_loc in self.tilemap:
                    tile = self.tilemap[tile_loc]
                    tile_type = tile['type']
                    tile_variant = tile['variant']
                    tile_pos = tile['pos']
                    display_tile = self.game.assets[tile_type][tile_variant]
                    display_tile = pygame.transform.scale(display_tile, (self.tile_size, self.tile_size))

                    display.blit(display_tile, (tile_pos[0] * self.tile_size - offset[0], tile_pos[1] * self.tile_size - offset[1]))

        # # Tiles that are rendered on the grid, visible and interactable
        # for tile in self.tilemap:
        #     tile_type = self.tilemap[tile]['type']
        #     tile_variant = self.tilemap[tile]['variant']
        #     tile_pos = self.tilemap[tile]['pos']
        #     display_tile = self.game.assets[tile_type][tile_variant]
        #     display_tile = pygame.transform.scale(display_tile, (self.tile_size, self.tile_size))

        #     display.blit(display_tile, (tile_pos[0] * self.tile_size - offset[0], tile_pos[1] * self.tile_size - offset[1]))