import pygame
import random
from scripts.system.entities import boss

class greenskin(boss):
    def __init__(self, image, position,enable=False,health=100):
        super().__init__(image, position,enable)
        self.health = health
    def copy(self):
        super().copy()
    def update(self):
        super().update()  
        self.shake(False)
    def render(self, display, offset=(0, 0)):
        super().render(display, offset)
    def check_mouse_collision(self,mouse_point):
        if self.enable:
            return pygame.Rect(self.position[0],self.position[1],self.image.img().get_width(),self.image.img().get_height()).collidepoint(mouse_point)
        return False
    def shake(self,shake = True):
        if shake:
            self.position = (self.position[0] + random.randint(-2,2),self.position[1] + random.randint(-2,2))
        else:
            self.position = (self.position[0] + random.randint(-1,1),self.position[1] + random.randint(-1,1))
    def take_damage(self,damage):
        self.shake(True)
        self.health -= damage
        if self.health <= 0:
            self.enable = False
            self.health = 0

          