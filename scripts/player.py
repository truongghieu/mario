from scripts.system.entities import object


class Player(object):
    def __init__(self, image, position,enable=False):
        super().__init__(image, position)
        self.move_speed = 2
        self.velocity = [0, 0]
    def update(self,movement=(0,0)):
        self.image.update()
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.position[0] += frame_movement[0]
        self.position[1] += frame_movement[1]
        
    def render(self, display, offset=(0, 0)):
        display.blit(self.image.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))
