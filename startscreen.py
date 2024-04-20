import pygame, sys

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.display = game.display
        self.clock = game.clock
        self.bg = game.assets["background"]
        self.width = 1200
        self.height = 675
        self.enter = False
        self.transparency = 0

    def draw_text(self, text, font_name, color, x, y, size):
        rgbt = list(color)
        rgbt.append(self.transparency)
        color = tuple(rgbt)
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, rgbt)
        

        # Creates a rectangle around the text surface, get the center of the rect
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        pygame.display.update()
    
    def update(self):
        if self.transparency == 255:
            self.transparency = 0
        else:
            self.transparency += 5

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.update()
        self.draw_text("Press SPACE to enter", "arialblack", (0, 0, 0), self.width/2, 550, 40)  # Adjust the position of the text
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.enter = True
        return self.enter