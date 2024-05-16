import pygame

class Safehouse:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.assets = game.assets
        self.player = game.player
        self.dialogues = game.dialogues
        self.movements = [False, False]
        self.playerprofile = [self.player.name, self.player.level, self.player.gold, self.player.HP, self.player.speed]

    def run(self):
        """Put your codes below"""
        print("Safehouse")