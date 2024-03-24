from scripts.system.entities import object
import pygame

class bullet(object):
    def __init__(self, image, position, velocity = [3,0],enabled = False):
        super().__init__(image, position)
        self.position = position
        self.velocity = velocity
        self.enabled = enabled
        self.dir = True
        self.bullet_distance = 20
        self.level = 0
    
    def update(self,pos = [0,0]):
        if self.dir:
            self.velocity[0] = -3
        else:
            self.velocity[0] = 3

        if abs(self.position[0] - pos[0]) > self.bullet_distance or abs(self.position[1] - pos[1]) > self.bullet_distance:
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
    
    def upgrade(self):
        self.level += 1
        if self.level == 1:
            self.bullet_distance = 20
        elif self.level == 2:
            self.bullet_distance = 30
        elif self.level == 3:
            self.bullet_distance = 40
            self.image = pygame.image.load("data/images/bullet2.png")
        elif self.level == 4:
            self.bullet_distance = 50
            self.image = pygame.image.load("data/images/bullet3.png")
        elif self.level == 5:
            self.bullet_distance = 60
            self.cooldown = 5
            self.image = pygame.image.load("data/images/bullet4.png")
                                           
    def reset(self):
        self.level = 0
        self.bullet_distance = 20
        self.image = pygame.image.load("data/images/bullet.png")