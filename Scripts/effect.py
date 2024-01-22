from scripts.system.entities import object

class effect(object):
    def __init__(self,image,position,enable=False):
        super().__init__(image,position)
        self.image = image.copy()
        self.enable = enable
        self.spawn_time = image.img_duration * len(self.image.images)
        self.current_time = self.spawn_time
    def reset(self):
        self.enable = False
        self.image.reset()

    def render(self,display,offset=(0,0)):
        if self.enable:
            display.blit(self.image.img(),(self.position[0]-offset[0],self.position[1]-offset[1]))
        else:
            display.blit(self.image.img(),(9999,9999))
    def update(self):
        if self.enable:
            self.image.update()
        else:
            self.image.reset()
            
        if self.image.done:
            self.image.reset()
            self.enable = False