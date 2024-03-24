from scripts.system.entities import object

import pygame

class collectable_object(object):
    def __init__(self, image, position, animation_speed=0.2):
        super().__init__(image, position)
        self.image = self.image[0]
        self.animation_timer = 20
        self.upped = True
        self.animation_speed = animation_speed

    def update(self,pos):
        self.animation_timer -= 1
        if self.animation_timer == 0:
            self.upped = not self.upped
            self.animation_timer = 20
        if self.upped:
            self.position = [self.position[0], self.position[1] + self.animation_speed]
        elif not self.upped:
            self.position = [self.position[0], self.position[1] - self.animation_speed]

        # check if collect 
        if self.rect().colliderect(pos):
            return True


    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
    def render(self, display, offset=(0, 0)):
        return super().render(display, offset)
    
class gold(collectable_object):
    def __init__(self, image, position, animation_speed=0.2):
        super().__init__(image, position, animation_speed)
        self.type = "gold"
    
    
class collectable_object_bullet_upgrade(collectable_object):
    def __init__(self, image, position, animation_speed=0.2):
        super().__init__(image, position, animation_speed)
        self.type = "bullet_upgrade"

    def upgrade(self,bullet,level):
        bullet.upgrade(level)


class collectable_object_player_upgrade(collectable_object):
    def __init__(self, image, position, animation_speed=0.2):
        super().__init__(image, position, animation_speed)
        self.type = "player_upgrade"

    def upgrade(self,player,level):
        player.upgrade(level)

class next_level(collectable_object):
    def __init__(self, image, position, animation_speed=0.2):
        super().__init__(image, position, animation_speed)
        self.type = "next_level"

    def next_level(self,game):
        game.next_level()

