import pygame, utils

cutscenes = {}

class Dialogues:
    def __init__(self, msgs, font, pos, size, speed, screen, img=None, color="black"):
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
        self.font = pygame.font.Font(font, size)
        self.snip = self.font.render("", True, self.color)

        self.status = {msg: False for msg in self.msgs}

    def draw(self):
        self.screen.blit(self.img, (0, 0))

        if self.done and self.lines < len(self.msgs) - 1:
            self.lines += 1
            self.msg = self.msgs[self.lines]
            self.frame = 0
            self.done = False
            self.pos[1] += self.size * 1.5

        elif self.done and self.lines == len(self.msgs) - 1:
            self.status[self.msg] = True

        if self.count < self.speed * len(self.msg):
            self.count += 1
        elif self.count >= self.speed * len(self.msg):
            self.done = True
            self.count = 0
        
        for lines in range(self.lines + 1):
            
            # Check if the message is printed once, if so print the whole message
            if self.status[self.msgs[lines]]:
                self.snip = self.font.render(self.msgs[lines], True, self.color)
                self.screen.blit(self.snip, self.pos)
            else:
                self.snip = self.font.render(self.msgs[lines][0:(self.frame // self.speed)], True, self.color)
            self.screen.blit(self.snip, (self.pos[0], self.pos[1] - (self.lines - lines) * self.size * 1.5))