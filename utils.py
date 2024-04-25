import pygame, os

# get the path of the current directory, if the directory is not in "Just A Game", add "Just A Game" to the path

def get_path():
    path = os.getcwd()
    if "Just-A-Game-G10" not in path:
        return "Just-A-Game-G10/"
    else:
        return ""
    
BASE_IMG_PATH = get_path() + "data/images/"
BASE_SCENE_PATH = get_path() + "data/cutscenes/"


def load_script(path):
    # gets the script from the cutscenes folder, return it as a list of strings
    with open(BASE_SCENE_PATH + path, "r") as f:
        return [line for line in f.read().split("\n") if line != ""]

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey("black")
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images

def scale_images(images, set_scale=None, scale=2):
    # scale up the images by 2 times (default scale) OR use set_scale to set the dimensions manually
    
    if type(images) != list:
        if set_scale != None:
            return pygame.transform.scale(images, set_scale)
        else:
            return pygame.transform.scale(images, (images.get_width() * scale, images.get_height() * scale))
    else:
        if set_scale != None:
            return [pygame.transform.scale(img, set_scale) for img in images]
        else:
            return [pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale)) for img in images]

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0 # refering to the frame of the game (1-60 frames per second)

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def img(self):
        # return the image of the current frame
        return self.images[int(self.frame / self.img_dur)]
    
    def update(self):
        if self.loop:
            # modulo frame by the total number of frames (each img dur * number of images)
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images)) 
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

# Might need to use pygame to scale up all the assets by 2 times
# Currently scaling up the assets manually in each file