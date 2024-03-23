from scripts.system.entities import object
import pygame

class bullet(object):
    def __init__(self, image, position, velocity = [3,0],enabled = False):
        super().__init__(image, position)
        self.position = position
        self.velocity = velocity
        self.enabled = enabled
        self.dir = True
    
    def update(self,pos = [0,0]):
        if self.dir:
            self.velocity[0] = -3
        else:
            self.velocity[0] = 3

        if abs(self.position[0] - pos[0]) > 100 or abs(self.position[1] - pos[1]) > 100:
            self.enabled = False
            self.position = [-100,-100]

        if self.enabled:
            self.position = [self.position[0] + self.velocity[0],self.position[1] + self.velocity[1]]
        else:
            self.position = [-100,-100]
    def render(self,surface,offset=(0,0)):
        surface.blit(self.image,(self.position[0] - offset[0],self.position[1] - offset[1]))
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], 8, 8)
