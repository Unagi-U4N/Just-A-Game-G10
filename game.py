# This part will be the main game loop and the main game logic
# Must be updated frequently to keep the game running smoothly
# Feel free to pull or inform me if you want to test our features from your branch

# Contributors: Ivan, Yuven, Putra

import pygame, sys
from utils import *
from startscreen import StartScreen
import play

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Just A Game')
        self.screen = pygame.display.set_mode((1200, 675))
        self.display = pygame.Surface((1200, 675))
        self.clock = pygame.time.Clock()

        self.assets= {
            "player": load_image("entities/player.png"),
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "large_decor": load_images("tiles/large_decor"),
            "background": load_image("background.png")

        }
        
        self.game = play.Play(self)
        self.startscreen = StartScreen(self)
        
        self.state = "start"

    def run(self):
        while True:
            
            self.display.fill((255,255,255))

            if self.state == "start":
                self.startscreen.run()
                if self.startscreen.enter:
                    self.state = "game"
                    self.startscreen.enter = False

            if self.state == "game":
                self.game.run()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()