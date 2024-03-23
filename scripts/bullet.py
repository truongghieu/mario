from scripts.system.entities import object


class bullet(object):
    def __init__(self, image, position, velocity):
        super().__init__(image, position)
        self.position = list(position)
        self.velocity = list(velocity)
    
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
    def render(self,surface,offset=(0,0)):
        surface.blit(self.image,(self.position[0] - offset[0],self.position[1] - offset[1]))
