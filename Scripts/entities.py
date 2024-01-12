import pygame

class object:
    def __init__(self, image, position):
        self.image = image
        self.position = position

    def render(self, display, offset=(0, 0)):
        display.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))   
    
    def update(self):
        pass    


class zombie(object):
    def __init__(self, image, position,enable=False):
        super().__init__(image, position)
        self.image = image.copy()
        self.enable = enable
        self.spawn_time = image.img_duration * len(self.image.images)
        self.current_time = self.spawn_time
    def update(self):
        if self.enable:
            self.image.update()
        if self.image.done:
            self.image.reset()
            self.enable = False

    def render(self, display, offset=(0, 0)):
        if self.enable:
            display.blit(self.image.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))
        else:
            display.blit(self.image.img(0), (self.position[0] - offset[0], self.position[1] - offset[1]))


    def copy(self):
        return zombie(self.image, self.position,self.enable)
    
    def check_mouse_collision(self,mouse_point):
        if self.enable:
            return pygame.Rect(self.position[0],self.position[1],self.image.img().get_width(),self.image.img().get_height()).collidepoint(mouse_point)
        return False
        