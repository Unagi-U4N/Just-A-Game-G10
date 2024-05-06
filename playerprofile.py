import pygame, csv
from utils import *
import random

saveprofile = False

# read profile
def read_profile(self):
        
# Read the csv file
        with open("playerprofile.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, col in enumerate(row):
                    self.draw_text(col, "arialblack", (0, 0, 0), 160 + i * 40, 250 + j * 40, 20)

    # Create profile
def create_profile(self):
        
        self.draw_text("Enter your name", "arialblack", (0, 0, 0), 160, 250, 40)
        self.draw_text("Press ENTER to confirm", "arialblack", (0, 0, 0), 160, 300, 40)
        exist = False

        with open("playerprofile.csv", "r") as file:
            for row in csv.reader(file):
                if self.name == row[0]:
                    self.draw_text("Profile already exists", "arialblack", (255, 0, 0), 160, 400, 40)
                    exist = True
                    
                    if not exist:
                        with open("playerprofile.csv", "a", newline="") as file:
                            self.saveprofile = True
                            writer = csv.writer(file)
                            writer.writerow([self.name, random.randint(1000, 9999), 1])
                            file.close()
                        
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    # only get alphabets
                    if event.unicode.isalpha():
                        self.name += event.unicode

        if self.saveprofile:
            self.draw_text("Profile created", "arialblack", (0, 0, 0), 160, 400, 40)
            self.name = ""
            pygame.display.update()

        self.draw_text(self.name, "arialblack", (0, 0, 0), 160, 350, 40)
        return self.saveprofile
