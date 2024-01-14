import pygame
from scripts.system.entities import object


class button(object):
    def __init__(self, image, position, enable=False):
        super().__init__(image, position)
        self.listeners = []
        
    def update(self):
        super().update()

    def render(self, display, offset=(0, 0)):
        super().render(display, offset)  
    
    def check_mouse_collision(self,mouse_point):
        if pygame.Rect(self.position[0],self.position[1],self.image.get_width(),self.image.get_height()).collidepoint(mouse_point):
            for listener in self.listeners:
                listener()

    def button_add_listener(self,listener):
        self.listeners.append(listener)