import pygame

BASE_IMG_PATH = "data/images/"

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey("black")
    return img