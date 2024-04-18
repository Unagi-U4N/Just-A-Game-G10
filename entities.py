
import pygame

class PhysicsEntity:

    # Size must be scaled with the same ratio as the original
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.character = self.game.assets[self.type]
        self.character = pygame.transform.scale(self.character, self.size)

        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, screen):
        screen.blit(self.character, self.pos)
