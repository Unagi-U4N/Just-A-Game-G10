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
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    # Update the movement of the player
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Collision detection, if the player collides with the tile, stop the player
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                    # print("collide right")
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                    # print("collide left")
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                    self.velocity[1] = 0
                    # print("collide bottom")
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                    self.velocity[1] = 0
                    # print("collide top")
                self.pos[1] = entity_rect.y

        # Gravity
        self.velocity[1] = min(10, self.velocity[1] + 0.2)

        # Reset the acceleration if the player is on the ground
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.character, (self.pos[0] - offset[0], self.pos[1] - offset[1]))