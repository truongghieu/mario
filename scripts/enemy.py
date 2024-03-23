from scripts.system.entities import object
import random
import pygame
class enemy(object):
    def __init__(self, image, position,state_cooldown = 50,size =8):
        super().__init__(image, position)  
        self.state_cooldown = state_cooldown
        self.state_cooldown_timer = self.state_cooldown
        self.dir = True
        self.size = size
        self.velocity = [0, 0]
        self.colisions = {"up":False,"down":False,"left":False,"right":False}
    def update(self,tilemap = None):

        self.image.update()
        self.colisions = {"up":False,"down":False,"left":False,"right":False}
        frame_movement = (self.velocity[0],  self.velocity[1])

        self.position[0] += frame_movement[0]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if self.rect().colliderect(rect):
                if frame_movement[0] > 0:
                    self.colisions["right"] = True
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    self.colisions["left"] = True
                    entity_rect.left = rect.right
                self.position[0] = entity_rect.x
        self.position[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if self.rect().colliderect(rect):
                if frame_movement[1] > 0:
                    self.colisions["down"] = True
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.colisions["up"] = True
                    entity_rect.top = rect.bottom
                self.position[1] = entity_rect.y

        self.velocity[1] = min(2,self.velocity[1] + 0.1)
        if self.colisions["down"] or self.colisions["up"]:
            self.velocity[1] = 0

        

    def render(self, surface, offset=(0, 0)):
        surface.blit(self.image.img(flip=not self.dir), (self.position[0] - offset[0], self.position[1] - offset[1]))

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size, self.size)
    

class snake(enemy):
    def __init__(self, image, position, state_cooldown=50, size=8):
        super().__init__(image, position, state_cooldown, size)
        self.state_cooldown = random.randint(50, 100)
        self.velocity = [0.2, 0]
    def update(self, tilemap=None):
        self.state_cooldown_timer -= 1
        if self.state_cooldown_timer < 0:
            self.state_cooldown_timer = self.state_cooldown
            self.dir = not self.dir
        self.velocity[0] = 0.2 if self.dir else -0.2
        super().update(tilemap)