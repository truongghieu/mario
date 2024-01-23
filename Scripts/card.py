from scripts.system.entities import object
import pygame
import math
class card(object):
    def __init__(self,image,position):
        super().__init__(image,position)
        self.is_flying = False
        self.target = None
        self.velocity = 5
        self.dir = None
        self.enable = True
        self.selected = False
    def render(self,display,offset=(0,0)):
        super().render(display,offset)
    def update(self):
        if self.is_flying:
            self.position = (self.position[0] + self.dir[0] * self.velocity,self.position[1] + self.dir[1] * self.velocity)
            if self.position[0] > self.target[0] - 10 and self.position[0] < self.target[0] + 10 and self.position[1] > self.target[1] - 10 and self.position[1] < self.target[1] + 10:
                self.is_flying = False
        

    def fly_to(self,position):
        if self.is_flying:
            self.enable = True
            return
        distance = math.sqrt( (position[0] - self.position[0])**2 + (position[1] - self.position[1])**2 )
        self.dir = ((position[0] - self.position[0])/distance,(position[1] - self.position[1])/distance )
        self.target = position
        self.is_flying = True

    def fly_out(self):
        self.fly_to((self.position[0],250))
        self.enable = False

    def check_mouse_collision(self,mouse_point):
        if self.enable:
            return pygame.Rect(self.position[0],self.position[1],self.image.get_width(),self.image.get_height()).collidepoint(mouse_point)
        return False
    def select(self):
        # scale to 1.1
        if not self.selected:
            self.selected = True
            self.position = (self.position[0],self.position[1] - 2)
    def deselect(self):
        if self.selected:
            self.selected = False
            self.position = (self.position[0],self.position[1] + 2)
