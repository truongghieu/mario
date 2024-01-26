from scripts.system.entities import object
import pygame
import math

class card_manager:
    def __init__(self,display,enable = False):
        self.cards = []
        self.display = display
        self.enable = enable
        self.card_positions = [(display.get_width()/2 - 32 - 64 -10,30),(display.get_width()/2 - 32,30),(display.get_width()/2 + 32 + 10,30)]
    def render(self):
        if self.enable:
            for card in self.cards:
                card.render(self.display)
    def update(self):
        if self.enable:
            for card in self.cards:
                card.update()
    def card_animation(self,pos):
        for card in self.cards:
            if card.check_mouse_collision(pos):
                card.select()
            else:
                card.deselect()
    def check_mouse_collision(self,mouse_point):
        for card in self.cards:
            if card.check_mouse_collision(mouse_point):
                for c in self.cards:
                    c.fly_out()
                card.card_function()
                break
        
        return None
    def add_card(self,card):
        self.cards.append(card)
    def remove_card(self,card):
        self.cards.remove(card)
    def start_card(self):
        # get 3 random cards from cards and enable them
        self.cards[0].enable = True
        self.cards[0].fly_to(self.card_positions[0])
        self.cards[1].enable = True
        self.cards[1].fly_to(self.card_positions[1])
        self.cards[2].enable = True
        self.cards[2].fly_to(self.card_positions[2])
        self.enable = True

class card(object):
    def __init__(self,image,position,handle = None):
        super().__init__(image,position)
        self.is_flying = False
        self.target = None
        self.velocity = 10
        self.dir = None
        self.enable = True
        self.selected = False
        self.handle = handle
    def render(self,display,offset=(0,0)):
        super().render(display,offset)
    def update(self):
        if self.enable:
            if self.is_flying:
                self.position = (self.position[0] + self.dir[0] * self.velocity,self.position[1] + self.dir[1] * self.velocity)
                if self.position[0] > self.target[0] - 10 and self.position[0] < self.target[0] + 10 and self.position[1] > self.target[1] - 10 and self.position[1] < self.target[1] + 10:
                    self.is_flying = False
            

    def fly_to(self,position):
        if self.is_flying:
            self.enable = True
            return
        distance = math.sqrt( (position[0] - self.position[0])**2 + (position[1] - self.position[1])**2 )
        distance = distance if distance != 0 else 1
        self.dir = ((position[0] - self.position[0])/distance,(position[1] - self.position[1])/distance )
        self.target = position
        self.is_flying = True
        self.enable = True
 

    def fly_out(self):
        self.fly_to((self.position[0],250))
        self.enable = True

    def check_mouse_collision(self,mouse_point):
        if self.enable:
            return pygame.Rect(self.position[0],self.position[1],self.image.get_width(),self.image.get_height()).collidepoint(mouse_point)
        return False
    def select(self):
        # scale to 1.1
        if not self.selected:
            self.selected = True
            self.position = (self.position[0],self.position[1] - 5)
    def deselect(self):
        if self.selected:
            self.selected = False
            self.position = (self.position[0],self.position[1] + 5)

    def card_function(self):
        pass

class card_score(card):
    def card_function(self):
        setattr(self.handle,"score",getattr(self.handle,"score") + 500)
        print(getattr(self.handle,"score"))
class card_damage(card):
    def card_function(self):
        setattr(self.handle.my_hammer,"dame",getattr(self.handle.my_hammer,"dame") + 1)
        print(getattr(self.handle.my_hammer,"dame"))

class card_zombie(card):
    def card_function(self):
        setattr(self.handle.zombie_manager_s,"zombie_count",getattr(self.handle.zombie_manager_s,"zombie_count") + 1)
        print(getattr(self.handle.zombie_manager_s,"zombie_count"))
