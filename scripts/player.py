from scripts.system.entities import object
import pygame

class Player(object):
    def __init__(self, root,image, position,size = 8):
        super().__init__(image,position)
        self.position = list(position)
        self.move_speed = 2
        self.player_health = 3
        self.velocity = [0, 0]
        self.size = size
        self.colisions = {"up":False,"down":False,"left":False,"right":False}
        self.air_time = 0
        self.root = root
        self.action = None
        self.animation = image
        self.flip = False
        self.jumps = 1
        self.double_jump = False
        self.auto_shoot = False
        self.shooting = False
        self.shooting_cooldown = 6
        self.shooting_cooldown_timer = self.shooting_cooldown 
        self.running = False

        self.level = 0

        self.shoot_pos = [self.position[0]+3,self.position[1] + 3]
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size, self.size)
    
    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.root.assets["player_"+str(action)].copy()
            self.animation.reset()

    def update(self,movement=(0,0),tilemap=None):
        self.shooting_cooldown_timer -= 1
        if self.auto_shoot and self.shooting_cooldown_timer < 0:
            self.shooting = True
            self.shooting_cooldown_timer = self.shooting_cooldown
        else:
            self.shooting = False
        self.shoot_pos = [self.position[0]+3,self.position[1] + 3]
        self.animation.update()
        self.colisions = {"up":False,"down":False,"left":False,"right":False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
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
       
        self.air_time += 1
        if self.colisions["down"]:
            self.air_time = 0
            self.jumps = 2 if self.double_jump else 1
            # print(self.air_time)
        if self.air_time > 4:
            if self.flip:
                self.set_action("jump_left")
            else:
                self.set_action("jump_right")
        else:
        
            if movement[1] - movement[0] > 0:
                self.set_action("run_left")
                self.flip = True
            if movement[1] - movement[0] < 0:
                self.set_action("run_right")
                self.flip = False
            if movement[1] - movement[0] == 0:
                if self.flip:
                    self.set_action("idle_left")
                else:
                    self.set_action("idle_right")
    def jump(self):
        if self.jumps > 0:
            self.velocity[1] = -2
            self.jumps -= 1
              
        
    def render(self, display, offset=(0, 0)):
        display.blit(self.animation.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))

    def reset(self):
        self.position = [50,50]
        self.velocity = [0,0]
        self.air_time = 0
        self.jumps = 1
        self.double_jump = False
        self.animation = self.root.assets["player_idle_right"].copy()
        self.shooting_cooldown = 6
        self.shooting_cooldown_timer = self.shooting_cooldown 

    def upgrade(self):
        self.level += 1
        if self.level == 1:
            self.double_jump = True
        elif self.level == 2:
            self.player_health += 1
        elif self.level == 3:
            self.shooting_cooldown = 4
        elif self.level == 4:
            self.shooting_cooldown = 2
        elif self.level == 5:
            self.shooting_cooldown = 1