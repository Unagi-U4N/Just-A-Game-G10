import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:

    # Size must be scaled with the same ratio as the original
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.character = self.game.assets[self.type]

        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        self.action = ""
        # self.anim_offset = (-6, -6) # offset for the animation rendering
        self.flip = False
        self.set_action("idle")

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action

            # Get the animation class
            self.animation = self.game.assets[self.type + "/" + action].copy()
            self.animation.frame = 0

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

        # Wallslide
        if (self.collisions["left"] or self.collisions["right"]) and not self.collisions["down"]:
            self.velocity[1] = min(1.5, self.velocity[1])

        # Set the movement flip
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Gravity
        self.velocity[1] = min(10, self.velocity[1] + 0.2)

        # Reset the acceleration if the player is on the ground
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, screen, offset=(0, 0)):
        screen.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.anim_offset = (-6, -6)

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        # Set the action of the player
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0

        if self.air_time > 4:
            if self.collisions["left"] or self.collisions["right"]:
                self.set_action("wall_slide")
            else:
                self.set_action("jump")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        # Set animation offset by (-6, -3) if the player's head collides with the ceiling
        if self.collisions["up"]:
            self.anim_offset = (-6, -3)
        elif self.collisions["down"] or self.collisions["left"] or self.collisions["right"]:
            self.anim_offset = (-6, -6)
        
