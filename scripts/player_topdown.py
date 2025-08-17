from scripts.system.entities import object
import pygame
from CONFIG import *

class topdown_player(object):
    def __init__(self, image, position):
        self.image = image
        self.position = list(position)
        self.speed = PLAYER_SPEED
        self.player_health = PLAYER_HEALTH
        self.colisions = {"up":False,"down":False,"left":False,"right":False}

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.image.img().get_width(), self.image.img().get_height())

    def render(self, display, offset=(0, 0)):
        display.blit(self.image.img(), (self.position[0] - offset[0], self.position[1] - offset[1]))

    def update(self, movement=(0,0), tilemap=None):
        self.colisions = {'up': False, 'down': False, 'left': False, 'right': False}
        
        move_vec = pygame.math.Vector2(movement)
        if move_vec.length_squared() != 0:
            move_vec.normalize_ip()
        
        frame_movement = (move_vec.x * self.speed, move_vec.y * self.speed)

        self.position[0] += frame_movement[0]
        entity_rect = self.rect()
        if tilemap:
            for rect in tilemap.physics_rects_around(self.position):
                if entity_rect.colliderect(rect):
                    if frame_movement[0] > 0:
                        entity_rect.right = rect.left
                        self.colisions['right'] = True
                    if frame_movement[0] < 0:
                        entity_rect.left = rect.right
                        self.colisions['left'] = True
                    self.position[0] = entity_rect.x

        self.position[1] += frame_movement[1]
        entity_rect = self.rect()
        if tilemap:
            for rect in tilemap.physics_rects_around(self.position):
                if entity_rect.colliderect(rect):
                    if frame_movement[1] > 0:
                        entity_rect.bottom = rect.top
                        self.colisions['down'] = True
                    if frame_movement[1] < 0:
                        entity_rect.top = rect.bottom
                        self.colisions['up'] = True
                    self.position[1] = entity_rect.y
