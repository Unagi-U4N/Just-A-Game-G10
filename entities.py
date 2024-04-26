import math
import random

import pygame
from particle import Particle
from spark import Spark


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, speed=2):
        self.speed = speed
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-6, -6)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Check for collisions with the tilemap
        self.pos = list(self.pos)
        self.pos[0] += frame_movement[0]*self.speed
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # Flip the sprite based on the movement
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(7, self.velocity[1] + 0.35)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

            self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0
        self.speed = 2
        self.difficulty = 3

        # self.projectile = 3
    
    def update(self, tilemap, movement=(0, 0)):

        if self.difficulty == 1:
            
            self.speed = 2
            dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
            if self.walking:
                # Check the 7 pixels in front, 23 pixels below of the enemy, if it's solid, turn around
                tile_loc = (self.rect().centerx + (-32 if self.flip else 32), self.pos[1] + 46)
                if tilemap.solid_check(tile_loc):

                    # If the player is within boundaries, not on top of the player, and there is no obstacle beside them, make the enemy turn around
                    if (self.collisions['right'] or self.collisions['left']):
                        self.flip = not self.flip

                    else:
                        # Move for 0.5 pixels every frame, until the walking counter reaches 0
                        movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])

                else:
                    self.flip = not self.flip

                self.walking = max(0, self.walking - 1)

                if not self.walking:
                    # get gunshot sparks and bullets
                    if (abs(dis[1]) < 32):
                        if (self.flip and dis[0] < 0):
                            self.game.projectiles.append([[self.rect().centerx - 14, self.rect().centery], -1 * self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random(), (255, 0, 0)))
                        if (not self.flip and dis[0] > 0):
                            self.game.projectiles.append([[self.rect().centerx + 14, self.rect().centery], self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random(), (255, 0, 0)))

            # 1 in 100 chance
            elif random.random() < 0.01:
                self.walking = random.randint(30, 120)

        elif self.difficulty == 2:
           
            self.speed = 3
            dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
            if self.walking:
                # Check the 7 pixels in front, 23 pixels below of the enemy, if it's solid, turn around
                tile_loc = (self.rect().centerx + (-32 if self.flip else 32), self.pos[1] + 46)
                if tilemap.solid_check(tile_loc):

                    # If the player is within boundaries, not on top of the player, and there is no obstacle beside them, make the enemy turn around
                    if (abs(dis[0]) < 100) and (abs(dis[1]) < 32) and not(self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        if (not self.flip and dis[0] < 0):
                            self.flip = not self.flip
                        if (self.flip and dis[0] > 0):
                            self.flip = not self.flip
                    
                    # If the player is out of boundaries, not on top of the player, and there is an obstacle beside them, make the enemy turn around
                    if not (abs(dis[0]) < 100) and not (abs(dis[1]) < 32) and (self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        self.flip = not self.flip

                    # If the player is in boundaries, there is obstacle, enemy is still running, stop the enemy immediately
                    if (abs(dis[0]) < 100) and (abs(dis[1]) < 32) and (self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        self.walking = 0

                    else:
                        # Move for 0.5 pixels every frame, until the walking counter reaches 0
                        movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])

                else:
                    # If there is a drop, and no players nearby, turn around
                    if (abs(dis[0]) > 100):
                        self.flip = not self.flip

                self.walking = max(0, self.walking - 1)

                if not self.walking:
                    # get gunshot sparks and bullets
                    if (abs(dis[1]) < 32):
                        if (self.flip and dis[0] < 0):
                            self.game.projectiles.append([[self.rect().centerx - 14, self.rect().centery], -1 * self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random(), (255, 0, 0)))
                        if (not self.flip and dis[0] > 0):
                            self.game.projectiles.append([[self.rect().centerx + 14, self.rect().centery], self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random(), (255, 0, 0)))

            # 1 in 100 chance
            elif random.random() < 0.01:
                self.walking = random.randint(30, 120)
        
        elif self.difficulty == 3:
           
            self.speed = 4
            dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
            if self.walking:
                # Check the 7 pixels in front, 23 pixels below of the enemy, if it's solid, turn around
                tile_loc = (self.rect().centerx + (-32 if self.flip else 32), self.pos[1] + 46)

                # If cooldown is 0, shoot
                if self.walking % 20 == 0:
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 14, self.rect().centery], -1 * self.speed, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random(), (255, 0, 0)))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 14, self.rect().centery], self.speed, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random(), (255, 0, 0)))

                if tilemap.solid_check(tile_loc):

                    # If the player is within boundaries, not on top of the player, and there is no obstacle beside them, make the enemy turn around
                    if (abs(dis[0]) < 300) and (abs(dis[1]) < 32) and not(self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        if (not self.flip and dis[0] < 0):
                            self.flip = not self.flip
                        if (self.flip and dis[0] > 0):
                            self.flip = not self.flip
                    
                    # If the player is out of boundaries, not on top of the player, and there is an obstacle beside them, make the enemy turn around
                    if not (abs(dis[0]) < 300) and (abs(dis[1]) < 32) and (self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        self.flip = not self.flip

                    # If the player is in boundaries, there is obstacle, enemy is still running, stop the enemy immediately
                    if (abs(dis[0]) < 300) and (abs(dis[1]) < 32) and (self.collisions['right'] or self.collisions['left']) and not (abs(dis[0]) == 0):
                        self.walking = 0

                    else:
                        # Move for 0.5 pixels every frame, until the walking counter reaches 0
                        movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])

                else:
                    # If there is a drop, and no players nearby, turn around
                    if (abs(dis[0]) > 300):
                        self.flip = not self.flip

                self.walking = max(0, self.walking - 1)

                if not self.walking:
                    # get gunshot sparks and bullets
                    if (abs(dis[1]) < 32) and (abs(dis[0]) < 300):
                        if (self.flip and dis[0] < 0):
                            self.game.projectiles.append([[self.rect().centerx - 14, self.rect().centery], -1 * self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random(), (255, 0, 0)))
                        if (not self.flip and dis[0] > 0):
                            self.game.projectiles.append([[self.rect().centerx + 14, self.rect().centery], self.speed, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random(), (255, 0, 0)))

            # 1 in 100 chance
            elif random.random() < 0.01:
                self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        # If the player is dashing, and the enemy collides with the player, kill the enemy
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.game.player.rect().center, angle, 2 + random.random(), (0,255,0)))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.game.player.rect().center, 0, 5 + random.random(), (0,0,255)))
                self.game.sparks.append(Spark(self.game.player.rect().center, math.pi, 5 + random.random(), (255,0,0)))
                return True

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets["gun"], True, False), (self.rect().centerx - 6 - self.game.assets["gun"].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets["gun"], (self.rect().centerx + 6 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.speed = 1.5 # default

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.air_time > 1200:
            if not self.game.dead:
                      self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 1.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        
        
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        # Dash is only 10 frames, the remaining 50 are for the cooldown
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 10

            # Once the dash reaches the end, stop abruptly
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        
        # During the dash
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
             angle = random.random() * math.pi * 2
             speed = random.random() * 0.5 + 0.5
             pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
             self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        
        # Slows down the repulsion after wall jump
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] -0.15, 0)
        else:
            self.velocity[0] = min(self.velocity[0] +0.15, 0)

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)

    def jump(self):
        # If wall jump, jump in the opposite direction of the wall and up, and reduce the amount of jumps left
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 6
                self.velocity[1] = -5
                self.air_time = 5
                self.jumps = max(0, self.jumps -1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -6
                self.velocity[1] = -5
                self.air_time = 5
                self.jumps = max(0, self.jumps -1)
                return True

        # If not wall jump, jump up and reduce the amount of jumps left
        elif self.jumps:
            self.velocity[1] = -7
            self.jumps -= 1
            self.air_time = 5
            return True
        
    def dash(self):

        # Cooldown = 60
        if not self.dashing:
            # self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
