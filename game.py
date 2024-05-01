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
        self.particles = []
        self.sparks = []    
        self.projectiles = []
        self.exclamation = []

        self.assets= {
            "player": load_image("entities/player.png"),
            "decor": scale_images(load_images("tiles/decor")),
            "grass": scale_images(load_images("tiles/grass")),
            "stone": scale_images(load_images("tiles/stone")),
            "large_decor": scale_images(load_images("tiles/large_decor")),
            "background": load_image("background/background.png"),
            "day": scale_images(load_image("background/daybg.png"), set_scale=(1200, 675)),
            "night": scale_images(load_image("background/nightbg.png"), set_scale=(1200, 675)),
            "clouds": load_images("clouds"),
            "player/idle": Animation(scale_images(load_images("entities/player/idle")), img_dur=2),
            "player/run": Animation(scale_images(load_images("entities/player/run")), img_dur=2),
            "player/jump": Animation(scale_images(load_images("entities/player/jump")), img_dur=2, loop=False),
            "player/slide": Animation(scale_images(load_images("entities/player/slide")), img_dur=2, loop=False),
            "player/wall_slide": Animation(scale_images(load_images("entities/player/wall_slide")), img_dur=2, loop=False),
            "enemy/idle": Animation(scale_images(load_images("entities/enemy/idle")), img_dur=2),
            "enemy/run": Animation(scale_images(load_images("entities/enemy/run")), img_dur=2),
            "particle/leaf": Animation(scale_images(load_images("particles/leaf")), img_dur=10, loop=False),
            "particle/particle": Animation(scale_images(load_images("particles/particle")), img_dur=4, loop=False),
            "gun": scale_images(load_image("gun.png")),
            "projectile": scale_images(load_image("projectile.png"), scale= 1.5),
            "!": scale_images(load_image("!.png"), scale= 0.8),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'wasted': pygame.mixer.Sound('data/sfx/wasted.wav'),
        }
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        self.sfx['wasted'].set_volume(1.5)
        
        self.game = play.Play(self)
        self.startscreen = StartScreen(self)
        
        self.state = "start"

    def run(self):
        while True:
        
            # pygame.mixer.music.load('data/music.wav')
            # pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)

            # self.sfx['ambience'].play(-1)
            
            if self.state == "start":
                newloadexit = self.startscreen.run()
                if newloadexit == "New Game":
                    self.state = "game"
                elif newloadexit == "Load Game":
                    pass
                elif newloadexit == "Exit Game":
                    pygame.quit()
                    sys.exit()

            if self.state == "game":
                self.game.run()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()