import os
#back 3 level
from ...CONFIG import *
import pygame


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self,index = None):
        if index != None:
            return self.images[index]
        return self.images[int(self.frame / self.img_duration)]

    def img(self,flip = False):
        if flip:
            return pygame.transform.flip(self.images[int(self.frame / self.img_duration)],True,False)
        return self.images[int(self.frame / self.img_duration)]

    def reset(self):
        self.frame = 0
        self.done = False

def mouse_rect_collision(mouse_pos):
    pygame.rect.Rect(mouse_pos[0],mouse_pos[1],1,1)

def convert_to_surface_pos(pos):
    return (pos[0] - 160,pos[1] - 120)
