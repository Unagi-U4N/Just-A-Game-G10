import pygame, os

# get the path of the current directory, if the directory is not in "Just A Game", add "Just A Game" to the path

def get_path():
    path = os.getcwd()
    if "Just A Game" not in path:
        return "Just-A-Game-G10/data/images/"
    else:
        return "data/images/"
    
BASE_IMG_PATH = get_path()

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey("black")
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images

# Might need to use pygame to scale up all the assets by 2 times
# Currently scaling up the assets manually in each file