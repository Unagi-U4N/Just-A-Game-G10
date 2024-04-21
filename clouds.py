import random, pygame
from utils import *

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.speed = speed
        self.depth = depth
        self.img = img
        self.img = scale_images(self.img, scale=2)
        self.img = pygame.transform.flip(self.img, True, False)

    def update(self):
        self.pos[0] -= self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloud_img, count=16):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud((random.random()*99999, random.random()*99999), random.choice(cloud_img), random.random()*0.1 + 0.1, random.random()*0.6 +0.4))

        self.clouds.sort(key=lambda x: x.depth) # Sort the clouds based on their depth, so that the further clouds are rendered first

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset)