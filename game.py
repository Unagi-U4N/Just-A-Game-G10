# This part will be the main game loop and the main game logic
# Must be updated frequently to keep the game running smoothly
# Feel free to pull or inform me if you want to test our features from your branch

# Contributors: Ivan, Yuven, Putra

import pygame, sys
from source.utils import *
from source.startscreen import StartScreen
from source.play import *
from source.playerprofile import *
import source.cutscenes
from source.music import Music

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Just A Game')
        self.shakescreen = pygame.display.set_mode((1200, 675))
        self.screen = self.shakescreen.copy()
        self.display = pygame.Surface((1200, 675))
        self.clock = pygame.time.Clock()
        self.loaded = False
        self.particles = []
        self.data = ["Ivan", "4", 10000, 2.5, 3, 1000]
        # self.data = []
        self.sparks = []    
        self.projectiles = []
        self.exclamation = []
        self.intro = {}
        self.font = "data/monogram.ttf"
        self.offset = repeat((0, 0))

        self.cutscenes = {
            "Intro": load_script("Intro"),
            "Ending": load_script("Ending"),
        }

        self.assets= {
            # "Name of the asset": scale_images(load_image("path to the asset"), scale= 1.5 OR set_scale=(1200, 675),
            "player": load_image("entities/player.png"),
            "npc": scale_images(load_image("entities/npc.png"), scale= 5),
            "decor": scale_images(load_images("tiles/decor")),
            "grass": scale_images(load_images("tiles/grass")),
            "stone": scale_images(load_images("tiles/stone")),
            "metal": scale_images(load_images("tiles/metal")),
            "glitch_blocks": scale_images(load_images("tiles/glitch blocks")),
            "large_decor": scale_images(load_images("tiles/large_decor")),
            "tile_background":scale_images(load_images("tiles/background")),
            "background": scale_images(load_image("background/background.png"), set_scale=(1200, 675)),
            "level_selection": scale_images(load_image("miscellaneous/level_selection.png"), set_scale=(1200, 675)),
            "level_1": scale_images(load_image("background/level1.png"), set_scale=(1200, 675)),
            "level_2": scale_images(load_image("background/level2.png"), set_scale=(1200, 675)),
            "level_3": scale_images(load_image("background/level3.png"), set_scale=(1200, 675)),
            "level_4": scale_images(load_image("background/level4.png"), set_scale=(1200, 675)),
            "save": scale_images(load_image("background/savescreen.png"), set_scale=(1200, 675)),
            "day": scale_images(load_image("background/daybg.png"), set_scale=(1200, 675)),
            "night": scale_images(load_image("background/nightbg.png"), set_scale=(1200, 675)),
            "clouds": load_images("clouds"),
            "safehousebg": scale_images(load_image("background/safehousebg.png"), set_scale=(1200, 675)),
            "cave": scale_images(load_image("background/cave.png"), set_scale=(1200, 675)),
            "cave_blocks": scale_images(load_images("tiles/cave blocks")),
            "newgamebg": scale_images(load_image("background/newgame.png"), set_scale=(1200, 675)),
            "player/idle": Animation(scale_images(load_images("entities/player/idle")), img_dur=2),
            "player/run": Animation(scale_images(load_images("entities/player/run")), img_dur=2),
            "player/jump": Animation(scale_images(load_images("entities/player/jump")), img_dur=2, loop=False),
            "player/slide": Animation(scale_images(load_images("entities/player/slide")), img_dur=2, loop=False),
            "player/wall_slide": Animation(scale_images(load_images("entities/player/wall_slide")), img_dur=2, loop=False),
            "enemy": scale_images(load_image("entities/enemy/idle/00.png")),
            "enemy/idle": Animation(scale_images(load_images("entities/enemy/idle")), img_dur=2),
            "enemy/run": Animation(scale_images(load_images("entities/enemy/run")), img_dur=2),
            "npc/idle": Animation(scale_images(load_images("entities/npc/idle")), img_dur=2),
            "particle/leaf": Animation(scale_images(load_images("particles/leaf")), img_dur=10, loop=False),
            "particle/particle": Animation(scale_images(load_images("particles/particle")), img_dur=4, loop=False),
            "core": Animation(scale_images(load_images("animation/core"), scale=1.5), img_dur=15, loop=False),
            "jump_sign": Animation(scale_images(load_images("animation/jump_sign")), img_dur=10, loop=True),
            "dash_sign": Animation(scale_images(load_images("animation/dash_sign")), img_dur=15, loop=True),
            "wall_slide_sign": Animation(scale_images(load_images("animation/wall_slide_sign")), img_dur=15, loop=True),
            "wall_jump_sign": Animation(scale_images(load_images("animation/wall_jump_sign")), img_dur=15, loop=True),
            "poison_sign": Animation(scale_images(load_images("animation/poison_sign")), img_dur=15, loop=True),
            "good_core": scale_images(load_image("animation/core/49.png"), scale= 1.5),
            "gun": scale_images(load_image("entities/enemy/gun.png")),
            "projectile": scale_images(load_image("entities/enemy/projectile.png"), scale= 1.5),
            "!": scale_images(load_image("entities/enemy/!.png"), scale= 0.8),
            "arrow": scale_images(load_image("indicators/arrow.png"), scale= 0.2),
            "arrow_w": scale_images(load_image("indicators/arrow_white.png"), scale= 0.2),
            "quit": scale_images(load_image("button/quit.png"), scale=0.5),
            "resume": scale_images(load_image("button/resume.png"), scale=0.5),
            "quit2": scale_images(load_image("button/quit2.png"), scale=0.5),
            "resume2": scale_images(load_image("button/resume2.png"), scale=0.5),
            "pausebuttonround": scale_images(load_image("button/pausebuttonround.png"), scale=0.15),
            "pause": scale_images(load_image("miscellaneous/pause.png"), set_scale=(1200, 675)),
            "ttt1": scale_images(load_image("ttt/ttt1.png"), set_scale=(1200, 675)),
            "ttt2": scale_images(load_image("ttt/ttt2.png"), set_scale=(1200, 675)),
            "ttt3": scale_images(load_image("ttt/ttt3.png"), set_scale=(1200, 675)),
            "X": scale_images(load_image("ttt/X.png"), scale= 0.5),
            "O": scale_images(load_image("ttt/O.png"), scale= 0.5),
            "controls1": scale_images(load_image("info/0.png"), set_scale=(1200, 675)),
            "controls2": scale_images(load_image("info/1.png"), set_scale=(1200, 675)),
            "controls3": scale_images(load_image("info/2.png"), set_scale=(1200, 675)),
            "controls4": scale_images(load_image("info/3.png"), set_scale=(1200, 675)),
            "info": scale_images(load_image("button/info.png"), scale=0.15),
            "buttonleft": scale_images(load_image("button/buttonleft.png"), scale= 1),
            "buttonright": scale_images(load_image("button/buttonright.png"), scale= 1),
            "loadgamebg": scale_images(load_image("background/loadgame.png"), set_scale=(1200, 675)),
            "delloadgamebg": scale_images(load_image("background/delloadgame.png"), set_scale=(1200, 675)),
            "profileup": scale_images(load_image("button/profileup.png"), scale= 0.5),
            "profiledown": scale_images(load_image("button/profiledown.png"), scale= 0.5),
            "dialoguebox": scale_images(load_image("miscellaneous/dialoguebox.png"), scale=0.7),
            "heart": scale_images(load_image("indicators/heart.png"), set_scale=(45, 40)),
            "heart1": scale_images(load_image("indicators/heart1.png"), set_scale=(45, 40)),
            "big-heart": scale_images(load_image("indicators/heart.png"), scale= 0.06),
            "big-shield": scale_images(load_image("indicators/shield.png"), scale= 0.08),
            "speed": scale_images(load_image("indicators/speed.png"), scale= 0.035),
            "gold": scale_images(load_image("indicators/gold.png"), scale= 0.08),
            "store": scale_images(load_image("store/store.png"), set_scale=(1200, 675)),
            "store_menu": scale_images(load_image("store/store_menu.png"), set_scale=(1200, 675)),
            "store_speed": scale_images(load_image("store/store_speed.png"), set_scale=(1200, 675)),
            "store_heart": scale_images(load_image("store/store_heart.png"), set_scale=(1200, 675)),
            "store_shield": scale_images(load_image("store/store_shield.png"), set_scale=(1200, 675)),
            "speed_potion": scale_images(load_image("indicators/speed_potion.png"), scale=0.2),
            "+": scale_images(load_image("indicators/+.png"), scale=0.07),
            "-": scale_images(load_image("indicators/-.png"), scale=0.07),
            "shield": scale_images(load_image("indicators/shield.png"), scale=0.05),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'wasted': pygame.mixer.Sound('data/sfx/wasted.wav'),
            "bullet": pygame.mixer.Sound('data/sfx/bullet.wav'),
            "click": pygame.mixer.Sound('data/sfx/click.wav'),
            "poison": pygame.mixer.Sound('data/sfx/poison.wav'),
        }
        
        self.sfx['ambience'].set_volume(0.05)
        self.sfx['shoot'].set_volume(0.6)
        self.sfx['hit'].set_volume(0.6)
        self.sfx['dash'].set_volume(1)
        self.sfx['jump'].set_volume(1)
        self.sfx['wasted'].set_volume(1)
        self.sfx['bullet'].set_volume(0.3)
        self.sfx['click'].set_volume(1)
        self.sfx['poison'].set_volume(0.2)
        
        self.startscreen = StartScreen(self)
        # self.game = Play(self)
        self.profile = PlayerProfile(self)
        self.music = Music(self)
        self.state = "game"
        self.cutscene = "Intro"

    def run(self):
        
        while True:

            if self.state == "start":
                newloadexit = self.startscreen.run()
                self.music.play_music("music")
                if newloadexit == "New Game":
                    self.state = "newgame"
                elif newloadexit == "Load Game":
                    self.state = "loadgame"
                elif newloadexit == "Exit Game":
                    pygame.quit()
                    sys.exit()

            elif self.state == "game":
                if not self.loaded:
                    self.game = Play(self)
                    self.game.load(self.data)
                    self.loaded = True
                self.game.run()
                self.music.play_music("music")

            elif self.state == "cutscene":
                self.state = "game"
                if self.cutscene == "Intro":
                    self.music.play_music("intense1")
                    cutscene = source.cutscenes.get_cutscene(self, "Intro", self.cutscenes, self.shakescreen)
                    source.cutscenes.runscenes(cutscene)
                elif self.cutscene == "Ending":
                    self.music.play_music("intense2")
                    cutscene = source.cutscenes.get_cutscene(self, "Ending", self.cutscenes, self.shakescreen)
                    source.cutscenes.runscenes(cutscene)

            elif self.state == "newgame":
                self.data = self.profile.create_profile()
                if type(self.data) is list:
                    self.state = "cutscene"
                    self.cutscene = "Intro"
                elif self.data == "start":
                    self.startscreen = StartScreen(self)
                    self.state = "start"
                elif self.data == "deleteprofile":
                    self.state = "deleteprofile"

            elif self.state == "loadgame":
                self.data = self.profile.read_profile()
                if type(self.data) is list:
                    self.state = "game"
                elif self.data == "start":
                    self.startscreen = StartScreen(self)
                    self.state = "start"

            elif self.state == "deleteprofile":
                state = self.profile.read_profile(delete=True)
                if type(state) is str:
                    self.startscreen = StartScreen(self)
                    self.state = "start"
                elif state:
                    self.state = "newgame"
            
            # Blit the screen over self.shakescreen with the offset
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            self.shakescreen.blit(self.screen, next(self.offset))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()