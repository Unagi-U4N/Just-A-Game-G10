import pygame, csv
from utils import *
import random

class PlayerProfile:
    def __init__(self, game):
        # self.img = game.assets["newgame"]
        self.game = game
        self.display = game.display
        self.name = ""
        self.names = []
        self.data = []
        self.saveprofile = False
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.bg = game.assets["newgame"]
        self.exist = False
            
    # read profile
    def read_profile(self):
            
    # Read the csv file
            with open("profile.csv", "r") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i == 0:
                        pass
                    for j, col in enumerate(row):
                        if j == 0:
                            # render_text(col, self.font, "black", 160, 400 + i * 40, self.display, centered=True)

        # Create profile
    def create_profile(self):
        with open("profile.csv", "r") as file:
            for row in csv.reader(file):
                if self.name == row[0]:
                    render_text("Profile already exists", self.font, "red", 600, 400, self.display, centered=True)
                    self.exist = True
                    print(self.exist)
                if len(self.name) > 10:
                    render_text("Profile name exceeds word limit", self.font, "red", 600, 400, self.display, centered=True)

            # Get player keyboard alphabet input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        
                        if not self.exist:
                            with open("profile.csv", "a", newline="") as file:
                                self.saveprofile = True
                                writer = csv.writer(file)
                                writer.writerow([self.name, 1, 0, 1.5, 3 ])
                                file.close()
                            
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        # only get alphabets
                        if event.unicode.isalpha():
                            self.name += event.unicode

            if self.saveprofile:
                self.data = [self.name, 1, 0, 1.5, 3]
                self.name = ""
                render_text("Profile created", self.font, "black", 600, 400, self.display, centered=True)
                pygame.display.update()
                return self.data

            render_text(self.name, self.font, "black", 600, 340, self.display, centered=True)
            
        
    def run(self, choice):
        self.display.blit(self.bg, (0,0))
        if choice == "new":
            self.create_profile()
        if choice == "load":
            self.read_profile()
        pygame.display.update()

    # def create_profile(self):
    #     if self.saveprofile:
    #         render_text("Profile created", pygame.font.Font('freesansbold.ttf', 72), "black", 160, 400, self.display, centered=True)
    #         self.name = ""
    #         pygame.display.update()

    #     render_text(self.name,  pygame.font.Font('freesansbold.ttf', 72), "black", 160, 400, self.display, centered=True)
    #     return self.saveprofile
