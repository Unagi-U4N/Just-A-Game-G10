import pygame

class Music:
    def __init__(self, game):
        self.game = game
        self.music = {
            "music": {
                "music": "data/music/music.wav",
            },
            "chill": {
                "chill0": "data/music/Chill/0.wav",
                "chill1": "data/music/Chill/1.wav",
                "chill2": "data/music/Chill/2.wav",
                "chill3": "data/music/Chill/3.wav",
                "chill4": "data/music/Chill/4.wav",
                "chill5": "data/music/Chill/5.wav"
            },
            "dream": {
                "dream0": "data/music/Dream/0.wav",
                "dream1": "data/music/Dream/1.wav",
                "dream2": "data/music/Dream/2.wav"
            },
            "intense": {
                "intense0": "data/music/Intense/0.wav",
                "intense1": "data/music/Intense/1.wav",
                "intense2": "data/music/Intense/2.wav",
                "intense3": "data/music/Intense/3.wav",
                "intense4": "data/music/Intense/4.wav",
                "intense5": "data/music/Intense/5.wav",
                "intense6": "data/music/Intense/6.wav",
                "intense7": "data/music/Intense/7.wav"
            },
            "noise": {
                "noise0": "data/music/Noise/0.wav",
                "noise1": "data/music/Noise/1.wav"
            }
        }
        self.current_music = ""
        self.music_playing = ""

    def play_music(self, folder, music):

        self.current_music = self.music[folder][music]
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