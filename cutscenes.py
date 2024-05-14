import pygame
from utils import *

# Get the top right coordinates of the dialogue box and return a tuple
dialoguebox_pos = (350, 490)

def get_dialogues(game, npc, dialogues, screen):

    # All the possible dialogues
    Dialogues = {
        "IntroP1": {},
        "IntroP2": {},
        "TicTacToe": {},
        "TicTacToeP2": {},
    }

    # cutscene(game, msgs, pos, size, speed, screen, img=None, color="white", choice)
    # Reason to this is to customize every single dialogue
    if npc == "IntroP1":
        Dialogues["IntroP1"]["0"] = Dialogue(game, "James", dialogues[npc]["0"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["0"][1], "black")
        Dialogues["IntroP1"]["1"] = Dialogue(game, "James", dialogues[npc]["1"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["1"][1], "black")
        Dialogues["IntroP1"]["2"] = Dialogue(game, "James", dialogues[npc]["2"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["2"][1], "black")

    elif npc == "IntroP2":
        Dialogues["IntroP2"]["0"] = Dialogue(game, "James", dialogues[npc]["0"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["0"][1], "black")
        Dialogues["IntroP2"]["1"] = Dialogue(game, "James", dialogues[npc]["1"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["1"][1], "black")
        Dialogues["IntroP2"]["2"] = Dialogue(game, "James", dialogues[npc]["2"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["2"][1], "black")
        Dialogues["IntroP2"]["3"] = Dialogue(game, "James", dialogues[npc]["3"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["3"][1], "black")
        Dialogues["IntroP2"]["4"] = Dialogue(game, "James", dialogues[npc]["4"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["4"][1], "black")
        Dialogues["IntroP2"]["5"] = Dialogue(game, "James", dialogues[npc]["5"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["5"][1], "black")
        Dialogues["IntroP2"]["6"] = Dialogue(game, "James", dialogues[npc]["6"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["6"][1], "black")
        Dialogues["IntroP2"]["7"] = Dialogue(game, "James", dialogues[npc]["7"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["7"][1], "black")
        Dialogues["IntroP2"]["8"] = Dialogue(game, "James", dialogues[npc]["8"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["8"][1], "black")
        Dialogues["IntroP2"]["9"] = Dialogue(game, "James", dialogues[npc]["9"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["9"][1], "black")
        Dialogues["IntroP2"]["10"] = Dialogue(game, "James", dialogues[npc]["10"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["10"][1], "black")
    
    elif npc == "TicTacToe":
        Dialogues["TicTacToe"]["0"] = Dialogue(game, "James", dialogues[npc]["0"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["0"][1], "black")
        Dialogues["TicTacToe"]["1"] = Dialogue(game, "James", dialogues[npc]["1"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["1"][1], "black")
        Dialogues["TicTacToe"]["2"] = Dialogue(game, "James", dialogues[npc]["2"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["2"][1], "black")
        Dialogues["TicTacToe"]["3"] = Dialogue(game, "James", dialogues[npc]["3"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["3"][1], "black")
    
    elif npc == "TicTacToeP2":
        Dialogues["TicTacToeP2"]["0"] = Dialogue(game, "James", dialogues[npc]["0"][0], (dialoguebox_pos), 30, 10, screen, dialogues[npc]["0"][1], "black")
    
    return Dialogues[npc]

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

def rundialogues(dialogues):
    num = 0
    repeat = False
    while not repeat:
        while num <= len(dialogues) - 1:     
            dialogue = str(num)
            skip = False
            next = False
            dialogue = dialogues[dialogue]
            dialogue.draw()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        skip = True
                        dialogue.fadescreen = 0
                        if skip and dialogue.done:
                            next = True

            if skip:
                dialogue.alldone = True

            if next and dialogue.done and skip:
                num += 1

        if num == len(dialogues):
            repeat = True
    
    # return True
                
def runscenes(scenes):
    # returns True if the cutscene is done
    # if choice is valid, returns choices made by the player
    num = 0
    while num <= len(scenes) - 1:     
        scene = str(num)
        skip = False
        next = False
        scene = scenes[scene]
        scene.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip = True
                    scene.fadescreen = 0
                    if skip and scene.done:
                        next = True

        if skip:
            scene.alldone = True

        if next and scene.done and skip:
            num += 1
    
    return True

def dialoguequestions(img, question, choices, screen):
    # Max number of choices is 3
    num = 0
    choice = None
    # Give a list of choices to the player, returns the choice made by the player
    answer = {choices[i]: False for i in range(len(choices))}
    while choice is None:
        render_img(img, 655, 550, screen)
        render_text(question, pygame.font.Font("data/monogram.ttf", 30), "black", dialoguebox_pos[0], dialoguebox_pos[1], screen, centered=False)
        for i in range(len(choices)):
            render_text(choices[i], pygame.font.Font("data/monogram.ttf", 30), "black", dialoguebox_pos[0] + 50, dialoguebox_pos[1] + 35 + i * 25, screen, centered=False)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    num = (num + 1) % len(choices)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    num = (num - 1) % len(choices)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    answer[choices[num]] = True
                    choice = choices[num]
        render_text(">", pygame.font.Font("data/monogram.ttf", 30), "black", dialoguebox_pos[0], dialoguebox_pos[1] + 35 + num * 25, screen, centered=False)
        pygame.display.flip()
        
    for choice in answer:
        if answer[choice] == True:
            choice = choice
            break

    return choice

class Logic:
    def __init__(self, game, msgs, pos, size, speed, screen, img=None, color="white"):
        self.fadescreenbool = False
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
        self.font = pygame.font.Font("data/monogram.ttf", self.size)
        self.snip = self.font.render("", True, self.color)
        self.status = {msg: False for msg in self.msgs}

    def draw(self):
        if  self.fadescreen > 0:
            self.fadescreenbool = True
        
        # check if the screen is fading
        if not self.fadescreenbool:

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
        
class Cutscene(Logic):
    def __init__(self, game, msgs, pos, size, speed, screen, img=None, color="white"):
        super().__init__(game, msgs, pos, size, speed, screen, img, color)

    def draw(self):
        super().draw()
        if self.fadescreenbool:
            self.fadescreen = max(0, self.fadescreen - 2)
            self.screen.blit(self.img, (0, 0))
            img = pygame.Surface((1200, 675))
            img.fill((0, 0, 0))
            img.set_alpha(self.fadescreen)
            self.screen.blit(img, (0, 0))
            pygame.display.flip()
            self.fadescreenbool = False

        if not self.fadescreenbool:

            if self.img != None:
                self.screen.blit(self.img, (0, 0))

            if self.alldone:
                self.status = {msg: True for msg in self.msgs}
                self.done = True
                render_img(self.game.assets["arrow"], 600, 600, self.screen,centered=True)
        

class Dialogue(Logic):
    def __init__(self, game, npc, msgs, pos, size, speed, screen, img=None, color="white"):
        super().__init__(game, msgs, pos, size, speed, screen, img, color)
        self.img = self.game.assets["dialoguebox"]
        self.fadescreenbool = False
        self.fadescreen = 0
        self.npc = img
        self.name = npc
        self.display = pygame.Surface((1200, 675))

    def draw(self):
        super().draw()
        # render_img(self.game.assets["day"], 0, 0, self.screen, centered=False)
        render_img(self.img, 655, 550, self.screen)
        render_img(scale_images(self.img, scale=0.2), 160, 610, self.screen)
        render_text(self.name, self.font, "black", 160, 610, self.screen, centered=True)
        render_img(self.npc, 155, 530, self.screen)

        if self.alldone:
            self.status = {msg: True for msg in self.msgs}
            self.done = True
            render_img(self.game.assets["arrow"], 1000, 550, self.screen,centered=True)