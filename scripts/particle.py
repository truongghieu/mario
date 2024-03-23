from scripts.system.entities import object
import random

class animate_object(object):
    def __init__(self, image, position,enabled = False):
        super().__init__(image, position)
        self.enabled = enabled
        self.dir = [0,0]
        self.image = self.image.copy()
        self.image.loop = False

    def update(self):
        # print(self.position)
        if self.enabled:
            self.position = [self.position[0] + self.dir[0],self.position[1] + self.dir[1]]
            self.image.update()
            if self.image.done:
                self.enabled = False
                self.image.reset()


    def render(self, surface, offset=(0, 0)):
        if not self.enabled:
            return
        surface.blit(self.image.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))


class particle(object):
    def __init__(self, image, position,quantity = 10,enabled = False):
        super().__init__(image, position)
        self.enabled = enabled
        self.quantity = quantity
        self.particles = []
        for i in range(self.quantity):
            self.particles.append(animate_object(self.image, self.position))
        
    def update(self):
        if self.enabled:
            for particle in self.particles:
                particle.image.reset()
                particle.position = self.position
                particle.dir = [float(random.randint(-5,5))/10,float(random.randint(-5,5))/10]
                particle.enabled = True
            self.enabled = False
        for particle in self.particles:
            particle.update()
       


    def render(self, surface, offset=(0, 0)):
        for particle in self.particles:
            particle.render(surface, offset)

class running_effect(particle):
    def __init__(self, image, position,quantity = 10,enabled = False):
        super().__init__(image, position,quantity,enabled)
        self.timer = 5
        
    def update(self):
        # print(self.enabled)
        self.timer -= 1
        if self.timer == 0:
            if self.enabled:
                for particle in self.particles:
                    if not particle.enabled:
                        particle.enabled = True
                        particle.image.reset()
                        particle.position = self.position
                        particle.dir = [float(random.randint(-5,5))/10,float(random.randint(-5,5))/10]
                        break
            self.enabled = False
            self.timer = 5


        for particle in self.particles:
            particle.update()
       


   