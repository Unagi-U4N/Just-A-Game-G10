import pygame

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
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                self.music_playing = self.current_music
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play(-1)