import pygame
from source.utils import *

class Music:
    def __init__(self, game):
        self.game = game
        self.music = {
            "music": "data/music/music.wav",
            "intense1": "data/music/intense1.wav",
            "intense2": "data/music/intense2.wav",
        }
        self.current_music = ""
        self.music_playing = ""

    def play_music(self, music):

        self.current_music = self.music[music]
        # Only play once when the music is changed
        if self.current_music != "":
            if self.current_music != self.music_playing:
                if self.music_playing != "":
                    self.game.display.fill((0, 0, 0))
                    render_img(self.game.assets["glitch_blocks"][5], 870, 600, self.game.display, True)
                    render_text("You can always create a new account if you are bored", pygame.font.Font(self.game.font, 36), "white", 600, 300, self.game.display, centered=True, transparency=255)
                    render_text("Loading...", pygame.font.Font(self.game.font, 50), (255, 255, 255), 1000, 600, self.game.display, True)
                    pygame.mixer.music.fadeout(2000)
                    # pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                self.music_playing = self.current_music
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)