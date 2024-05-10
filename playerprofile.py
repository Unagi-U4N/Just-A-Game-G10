import pygame, csv
from utils import *
import random

class PlayerProfile:
    def __init__(self, game):
        self.warning = False
        self.warningtimer = 0
        self.timer = 0
        self.game = game
        self.display = game.display
        self.profiles = []
        self.name = ""
        self.data = []
        self.saveprofile = False
        self.loaded = False
        self.choose = False
        self.font = pygame.font.Font(self.game.font, 60)
        self.newbg = game.assets["newgamebg"]
        self.loadbg = game.assets["loadgamebg"]
        self.delloadbg = game.assets["delloadgamebg"]
        self.exist = False
            
    # read profile
    def read_profile(self, delete=False):
        if delete:
            self.display.blit(self.delloadbg, (0,0))
        else:
            self.display.blit(self.loadbg, (0,0))
        # Read the csv file
        if not self.loaded:
            with open("profile.csv", "r") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i == 0 or i > 8:
                        pass
                    else:
                        # Append the profile to the list
                        # Name, lvl, gold, speed, HP
                        self.profiles.append([row[0], row[1], row[2], row[3], row[4]])
                        self.loaded = True
    
        # for i in range(numofbutton):
        for i in range(len(self.profiles)):
            render_text(str(i+1)+"   "+self.profiles[i][0], self.font, "black", 350 if i <= 3 else 650, (225 + i * 50) if i <= 3 else (225 + i * 50 - 200), self.display, centered=False)

        for j in range (8 - len(self.profiles)):
            render_text(str(j+1+len(self.profiles))+"   ---", self.font, "black", 350 if j+1+len(self.profiles) <= 4 else 650, (225 + (j + len(self.profiles)) * 50) if j+1+len(self.profiles) <= 4 else (225 + (j + len(self.profiles)) * 50 - 200), self.display, centered=False)

        # Get player keyboard input (1-8)
        profile = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_1:
                    if len(self.profiles) > 0:
                        profile = 0
                    else:
                        self.warning = True
                elif event.key == pygame.K_2:
                    if len(self.profiles) > 1:
                        profile = 1
                    else:
                        self.warning = True
                elif event.key == pygame.K_3:
                    if len(self.profiles) > 2:
                        profile = 2
                    else:
                        self.warning = True
                elif event.key == pygame.K_4:
                    if len(self.profiles) > 3:
                        profile = 3
                    else:
                        self.warning = True
                elif event.key == pygame.K_5:
                    if len(self.profiles) > 4:
                        profile = 4
                    else:
                        self.warning = True
                elif event.key == pygame.K_6:
                    if len(self.profiles) > 5:
                        profile = 5
                    else:
                        self.warning = True
                elif event.key == pygame.K_7:
                    if len(self.profiles) > 6:
                        profile = 6
                    else:
                        self.warning = True
                elif event.key == pygame.K_8:
                    if len(self.profiles) > 7:
                        profile = 7
                    else:
                        self.warning = True
                elif event.key == pygame.K_ESCAPE:
                    return "start"

        if self.warning:
            render_text("Profile not found", self.font, "red", 600, 450, self.display, centered=True)
            self.warningtimer += 1
            if self.warningtimer >= 60:
                self.warning = False
                self.warningtimer = 0
        
        self.data = self.profiles[profile] if profile is not None else []

        if not delete:
            if self.data != []:
                self.data[1] = int(self.data[1])
                self.data[2] = int(self.data[2])
                self.data[3] = float(self.data[3])
                self.data[4] = int(self.data[4])
                render_text(f"Profile {self.data[0]} loaded", self.font, "black", 600, 450, self.display, centered=True)
                self.timer += 1
                if self.timer >= 120:
                    return self.data
        
        if delete:
            deleted = False
            with open("profile.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Level", "Gold", "Speed", "HP"])
                for row in self.profiles:
                    if self.data in self.profiles:
                        self.profiles.remove(self.data)
                        deleted = True
                    writer.writerow(row)
                file.close()

            return deleted
        
        pygame.display.update()

        # Create profile
    def create_profile(self):
        self.display.blit(self.newbg, (0,0))
        with open("profile.csv", "r") as file:
            numofprofiles = len(list(csv.reader(file)))
            file.close()
        with open("profile.csv", "r") as file:
            for row in csv.reader(file):
                if numofprofiles > 8 and not self.saveprofile:
                    render_text("Profile limit reached", self.font, "red", 600, 400, self.display, centered=True)
                    render_text("Please delete a profile", self.font, "red", 600, 450, self.display, centered=True)
                    self.warningtimer += 1
                    if self.warningtimer >= 1000:
                        self.warningtimer = 0
                        return "deleteprofile"
                elif self.name == row[0] and not self.saveprofile:
                    render_text("Profile already exists", self.font, "red", 600, 400, self.display, centered=True)
                    self.exist = True
                elif self.name == "":
                    render_text("Profile name cannot be empty", self.font, "red", 600, 400, self.display, centered=True)
                    self.exist = True
                elif len(self.name) >= 7:
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
                                writer.writerow([self.name, 0, 0, 1.5, 3])
                                file.close()
                            
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]

                    elif event.key == pygame.K_ESCAPE:
                        self.name = ""
                        return "start"
                    
                    else:
                        # only get alphabets
                        if event.unicode.isalpha() and len(self.name) < 7:
                            self.name += event.unicode

            if self.saveprofile:
                self.data = [self.name, 0, 0, 1.5, 3]
                render_text("Profile created", self.font, "black", 600, 400, self.display, centered=True)
                pygame.display.update()
                self.timer += 1
                if self.timer >= 120:
                    return self.data

            render_text(self.name, self.font, "black", 600, 340, self.display, centered=True)
            pygame.display.update()
            