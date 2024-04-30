import pygame, json

NEIGHBOURS_OFFSETS = [(-1, -1), (-1, 0), (-1,1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
PHYSICS_TILES = {"stone", "grass"}

class Tilemap:
    # Create a tilemap with a grid of tiles size 16x16 (default)
    def __init__(self, game, tile_Size=32):
        self.game = game
        self.tile_size = tile_Size
        self.tilemap = {}
        self.offgrid_tiles = []

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def extract(self, id_pairs, keep=False):
        # Get all the tiles that match the id_pairs
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap.copy():
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = tuple(list(matches[-1]['pos']).copy())
                matches[-1]['pos'] = (matches[-1]['pos'][0] * self.tile_size, matches[-1]['pos'][1] * self.tile_size)
                if not keep:
                    del self.tilemap[loc]
        
        return matches

    def tiles_around(self, pos):
        # Get the location of the tile in the grid based on the position of the player
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOURS_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rect = []
        # If the tile is a physics tile, add rect to it
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rect.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
        return rect

    def render(self, display, offset=(0, 0), player_pos=(0, 0)):

        """
        Needs optimization, try to only render whats on the screen, instead of everything
        Maybe can check the location of the player (center) as reference, and only render what is visible
        """
        self.count = 0
        self.xcount = 0
        player_pos = int(player_pos[0]), int(player_pos[1])
        for tile in self.offgrid_tiles:
            self.xcount += 1
            if tile["pos"][0] in range(player_pos[0] - display.get_width() // 2 - 300, player_pos[0] + display.get_width() // 2 + 300) and tile["pos"][1] in range(player_pos[1] - display.get_height() // 2 - 300, player_pos[1] + display.get_height() // 2 + 300):
                display.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                self.count += 1

        print("Offgrid tiles: " + str(self.xcount))
        print("Offgrid tiles rendered: " + str(self.count))
            
        # For all of the tiles that are visible on the screen, render them
        # Tiles that are rendered on the grid, visible and interactable
        for x in range(offset[0] // self.tile_size, (offset[0] + display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + display.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    display.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        # print("Ongrid tiles: " + str(self.tilecount))