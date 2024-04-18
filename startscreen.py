import pygame, sys

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.display = game.display
        self.clock = game.clock
        self.bg = game.assets["background"]
        self.bg = pygame.transform.scale(self.bg, (400, 225))
        self.enter = False

    def draw_text(self, text, font_name, color, x, y, size):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        pygame.display.update()

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.draw_text("Press SPACE to enter", "arialblack", (0, 0, 0), 20, 20, 5)  # Adjust the position of the text
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.enter = True
        return self.enter