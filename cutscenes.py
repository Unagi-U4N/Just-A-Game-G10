import pygame
from utils import *

def get_cutscene(game, type, cutscenes, screen):
    
    Cutscenes = {"Intro": {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None, "9": None},
                "Ending": {"0": None}
                }

    # cutscene(game, msgs, pos, size, speed, screen, img=None, color="white")
    
    if type == "Intro":
        Cutscenes["Intro"]["0"] = Cutscene(game, cutscenes[type]["0"][0], (518, 480), 45, 40, screen, cutscenes[type]["0"][1])
        Cutscenes["Intro"]["1"] = Cutscene(game, cutscenes[type]["1"][0], (75, 180), 40, 20, screen, cutscenes[type]["1"][1])
        Cutscenes["Intro"]["2"] = Cutscene(game, cutscenes[type]["2"][0], (100, 420), 40, 20, screen, cutscenes[type]["2"][1])       
        Cutscenes["Intro"]["3"] = Cutscene(game, cutscenes[type]["3"][0], (130, 230), 40, 20, screen, cutscenes[type]["3"][1])     
        Cutscenes["Intro"]["4"] = Cutscene(game, cutscenes[type]["4"][0], (50, 190), 40, 20, screen, cutscenes[type]["4"][1])  
        Cutscenes["Intro"]["5"] = Cutscene(game, cutscenes[type]["5"][0], (50, 250), 40, 20, screen, cutscenes[type]["5"][1]) 
        Cutscenes["Intro"]["6"] = Cutscene(game, cutscenes[type]["6"][0], (110, 270), 40, 20, screen, cutscenes[type]["6"][1])             
        Cutscenes["Intro"]["7"] = Cutscene(game, cutscenes[type]["7"][0], (110, 250), 40, 20, screen, cutscenes[type]["7"][1])
        Cutscenes["Intro"]["8"] = Cutscene(game, cutscenes[type]["8"][0], (110, 210), 40, 20, screen, cutscenes[type]["8"][1]) 
        Cutscenes["Intro"]["9"] = Cutscene(game, cutscenes[type]["9"][0], (350, 300), 40, 40, screen, cutscenes[type]["9"][1])   
    
    elif type == "Ending":
        Cutscenes["Ending"]["0"] = Cutscene(game, cutscenes[type]["0"][0], (50, 50), 20, 50, screen, cutscenes[type]["0"][1])

    return Cutscenes[type]

def run(scenes, fade=False):
    num = 0
    while num <= len(scenes) - 1:
        scene = str(num)
        skip = False
        next = False
        scene = scenes[scene]
        scene.draw(fade)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip = True
                    if skip and scene.done:
                        next = True

        if skip:
            scene.alldone = True

        if next and scene.done and skip:
            num += 1
    
    return True

class Cutscene:
    def __init__(self, game, msgs, pos, size, speed, screen, img=None, color="white"):
        self.fadescreen = 255
        self.game = game
        self.msgs = msgs
        self.lines = 0
        self.msg = self.msgs[self.lines]
        self.color = color
        self.pos = list(pos)
        self.speed = speed
        self.screen = screen
        self.img = img
        self.frame = 0
        self.done = False
        self.alldone = False
        self.size = size
        self.font = pygame.font.Font(self.game.font, self.size)
        self.snip = self.font.render("", True, self.color)
        self.status = {msg: False for msg in self.msgs}

    def draw(self, fade=False):

        if fade and self.fadescreen > 0:
            self.fadescreen = max(0, self.fadescreen - 2)
            self.screen.blit(self.img, (0, 0))
            img = pygame.Surface((1200, 675))
            img.fill((0, 0, 0))
            img.set_alpha(self.fadescreen)
            self.screen.blit(img, (0, 0))
            pygame.display.flip()
        
        else:
            
            self.screen.blit(self.img, (0, 0))

            if self.alldone:
                self.status = {msg: True for msg in self.msgs}
                self.done = True
                render_img(self.game.assets["arrow"], 600, 600, self.screen,centered=True)
            
            # If the first line of message is done, and there is still message beneath, move to the next line
            if self.done and self.lines < len(self.msgs) - 1:
                self.status[self.msg] = True
                self.lines += 1
                self.msg = self.msgs[self.lines]
                self.frame = 0
                self.done = False
                self.pos[1] += self.size * 1.5

            elif self.done and self.lines == len(self.msgs) - 1:
                self.status[self.msg] = True

            if self.frame < self.speed * len(self.msg):
                self.frame += 1

            elif self.frame >= self.speed * len(self.msg):
                self.done = True
            
            for lines in range(self.lines + 1):
                
                # Check if the message is printed once, if so print the whole message
                if self.status[self.msgs[lines]]:
                    self.snip = self.font.render(self.msgs[lines], True, self.color)
                else:
                    self.snip = self.font.render(self.msgs[lines][0:(self.frame // self.speed)], True, self.color)
                self.screen.blit(self.snip, (self.pos[0], self.pos[1] - (self.lines - lines) * self.size * 1.5))

            if all([self.status[msg] for msg in self.msgs]):
                self.alldone = True
            
            pygame.display.flip()
        