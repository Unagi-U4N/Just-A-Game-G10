import pygame
from utils import *

cutscenes = {
    "Intro": load_script("Intro"),
}

class Cutscene:
    def __init__(self, msgs, pos, size, speed, screen, img=None, color="white"):
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
        self.font = pygame.font.Font("freesansbold.ttf", self.size)
        self.snip = self.font.render("", True, self.color)
        self.status = {msg: False for msg in self.msgs}

    def draw(self):
        # self.screen.blit(self.img, (0, 0))
        self.screen.fill((0, 0, 0))

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
        
        if self.alldone:
            for msg in self.msgs:
                self.status[msg] = True

        pygame.display.flip()

def get_cutscene(scenes, screen):
    
    Intro = {}
    

    for scene in cutscenes["Intro"]:
        Intro[scene] = Cutscene(cutscenes["Intro"][scene][0], (50, 50), 20, 50, screen, cutscenes["Intro"][scene][1].convert())

    if scenes == "Intro":
        return Intro

def run_cutscene(cutscene):
    num = 0
    while num <= len(cutscene) - 1:
        scene = str(num)
        skip = False
        next = False
        scene = cutscene[scene]
        scene.draw()
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
