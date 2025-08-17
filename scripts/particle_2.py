from scripts.system.entities import object


class animating_object(object):
    def __init__(self, image, position):
        super().__init__(image, position)
        
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.image.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))
        

    def update(self):
        self.image.update()
        pass

