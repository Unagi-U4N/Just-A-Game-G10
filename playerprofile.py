import pygame, csv
from utils import *
import random

class PlayerProfile:
    def __init__(self, game):
        self.timer = 0
        self.game = game
        self.display = game.display
        self.profiles = []
        self.name = ""
        self.data = []
        self.saveprofile = False
        self.font = pygame.font.Font(self.game.font, 60)
        self.newbg = game.assets["newgamebg"]
        self.loadbg = game.assets["loadgamebg"]
        self.exist = False
            
    # read profile
    def read_profile(self):
        self.display.blit(self.loadbg, (0,0))
        # Read the csv file
        with open("profile.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                # Append the profile to the list
                # Name, lvl, gold, speed, HP
                self.profiles.append([row[0], row[1], row[2], row[3], row[4]])

        numofbutton = min(len(self.profiles), 4)
        for i in range(numofbutton):
            render_img(self.game.assets["profileup"], 600, 200 + i * 100, self.display)

                        

        # Create profile
    def create_profile(self):
        self.display.blit(self.newbg, (0,0))
        with open("profile.csv", "r") as file:
            for row in csv.reader(file):
                if self.name == row[0] and not self.saveprofile:
                    render_text("Profile already exists", self.font, "red", 600, 400, self.display, centered=True)
                    self.exist = True
                if len(self.name) >= 10:
                    render_text("Profile name too long", self.font, "red", 600, 400, self.display, centered=True)
                    self.exist = True
                else:
                    self.exist = False

            # Get player keyboard alphabet input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        
                        if not self.exist:
                            with open("profile.csv", "a", newline="") as file:
                                self.saveprofile = True
                                writer = csv.writer(file)
                                writer.writerow([self.name, 0, 0, 1.5, 3 ])
                                file.close()
                            
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        # only get alphabets
                        if event.unicode.isalpha() and len(self.name) < 10:
                            self.name += event.unicode

            if self.saveprofile:
                self.data = [self.name, 0, 0, 1.5, 3]
                render_text("Profile created", self.font, "black", 600, 400, self.display, centered=True)
                pygame.display.update()
                self.timer += 1
                if self.timer >= 120:
                    return self.data

            render_text(self.name, self.font, "black", 600, 340, self.display, centered=True)
            
        
    def run(self, choice):
        if choice == "new":
            return self.create_profile()
        if choice == "load":
            self.read_profile()
        pygame.display.update()