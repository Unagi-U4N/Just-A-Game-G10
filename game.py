# This part will be the main game loop and the main game logic
# Must be updated frequently to keep the game running smoothly
# Feel free to pull or inform me if you want to test our features from your branch

# Contributors: Ivan, Yuven, Putra

import pygame, sys
from utils import *
from startscreen import StartScreen
from play import *
from playerprofile import *
import cutscenes

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Just A Game')
        self.screen = pygame.display.set_mode((1200, 675))
        self.display = pygame.Surface((1200, 675))
        self.clock = pygame.time.Clock()
        self.font = "data/monogram.ttf"
        self.loaded = False
        self.particles = []
        self.data = ["a", 0, 100, 3, 3]
        self.sparks = []    
        self.projectiles = []
        self.exclamation = []
        self.intro = {}
        self.font = "data/monogram.ttf"

        self.cutscenes = {
            "Intro": load_script("Intro"),
        }
        
        self.assets= {
            "player": load_image("entities/player.png"),
            "decor": scale_images(load_images("tiles/decor")),
            "grass": scale_images(load_images("tiles/grass")),
            "stone": scale_images(load_images("tiles/stone")),
            "large_decor": scale_images(load_images("tiles/large_decor")),
            "background": load_image("background/background.png"),
            "loadscreen1": load_image("loadscreen1.png"),
            "loadscreen2": load_image("loadscreen2.png"),
            "day": scale_images(load_image("background/daybg.png"), set_scale=(1200, 675)),
            "night": scale_images(load_image("background/nightbg.png"), set_scale=(1200, 675)),
            "clouds": load_images("clouds"),
            "newgamebg": scale_images(load_image("background/newgame.png"), set_scale=(1200, 675)),
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
            "arrow": scale_images(load_image("arrow.png"), scale= 2),
            "quit": scale_images(load_image("button/quit.png"), scale=0.5),
            "resume": scale_images(load_image("button/resume.png"), scale=0.5),
            "quit2": scale_images(load_image("button/quit2.png"), scale=0.5),
            "resume2": scale_images(load_image("button/resume2.png"), scale=0.5),
            "pausebuttonround": scale_images(load_image("button/pausebuttonround.png"), scale=0.15),
            "pause": scale_images(load_image("pause.png"), set_scale=(1200, 675)),
            "controls": scale_images(load_image("controls.png"), set_scale=(1200, 675)),
            "info": scale_images(load_image("button/info.png"), scale=0.15),
            "buttonleft": scale_images(load_image("button/buttonleft.png"), scale= 1),
            "buttonright": scale_images(load_image("button/buttonright.png"), scale= 1),
            "loadgamebg": scale_images(load_image("background/loadgame.png"), set_scale=(1200, 675)),
            "delloadgamebg": scale_images(load_image("background/delloadgame.png"), set_scale=(1200, 675)),
            "profileup": scale_images(load_image("button/profileup.png"), scale= 0.5),
            "profiledown": scale_images(load_image("button/profiledown.png"), scale= 0.5),
            "heart": scale_images(load_image("indicators/heart.png"), scale= 0.035),
            "speed": scale_images(load_image("indicators/speed.png"), scale= 0.035),
            "gold": scale_images(load_image("indicators/gold.png"), scale= 0.035),

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
        
        self.startscreen = StartScreen(self)
        self.game = Play(self)
        self.profile = PlayerProfile(self)
        self.state = "game"
        self.cutscene = "Intro"

    def run(self):
        while True:
        
            # pygame.mixer.music.load('data/music.wav')
            # pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)

            # self.sfx['ambience'].play(-1)
            
            if self.state == "start":
                newloadexit = self.startscreen.run()
                if newloadexit == "New Game":
                    self.state = "newgame"
                elif newloadexit == "Load Game":
                    self.state = "loadgame"
                elif newloadexit == "Exit Game":
                    pygame.quit()
                    sys.exit()

            if self.state == "game":
                if not self.loaded:
                    self.game.load(self.data)
                    self.loaded = True
                self.game.run()

            if self.state == "newgame":
                self.data = self.profile.create_profile()
                if type(self.data) is list:
                    self.state = "cutscene"
                    self.cutscene = "Intro"
                if self.data == "start":
                    self.startscreen = StartScreen(self)
                    self.state = "start"
                if self.data == "deleteprofile":
                    self.state = "deleteprofile"

            if self.state == "loadgame":
                self.data = self.profile.read_profile()
                if type(self.data) is list:
                    self.state = "game"
                elif self.data == "start":
                    self.startscreen = StartScreen(self)
                    self.state = "start"

            if self.state == "deleteprofile":
                state = self.profile.read_profile(delete=True)
                if type(state) is str:
                    self.startscreen = StartScreen(self)
                    self.state = "start"
                elif state:
                    self.state = "newgame"
    
            if self.state == "cutscene":
                if self.cutscene == "Intro":
                    cutscene = cutscenes.get_cutscene(self, "Intro", self.cutscenes, self.screen)
                    cutscenes.run(cutscene, True)
                    self.state = "game"
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()