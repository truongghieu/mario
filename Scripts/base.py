from scripts.system.entities import object
import random
class base(object):
    def __init__(self,image,position):
        super().__init__(image,position)
        self.defaut_pos = position
        self.shake_duration = 4
        self.current_shake_duration = 0
        self.shake_done = True
        self.strenght = 1
    def render(self,display,offset=(0,0)):
        super().render(display,offset)
    def update(self):
        # if self.shake():
        #     self.position = self.defaut_pos
        if self.shake_duration > self.current_shake_duration and not self.shake_done:
            self.current_shake_duration += 1
            self.position = (self.defaut_pos[0] + random.randint(-self.strenght,self.strenght),self.defaut_pos[1] + random.randint(-self.strenght,self.strenght))
        else:
            self.shake_done = True
            self.current_shake_duration = 0
            self.position = self.defaut_pos
    def shake(self,strenght = 1):
        self.strenght = strenght
        self.shake_done = False
        