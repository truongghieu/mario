from scripts.system.entities import object
import math
import pygame


UNSELECTED = "red"
SELECTED = "white"

BUTTONSTATES = {
    True:SELECTED,
    False:UNSELECTED
}

class panel(object):
    def __init__(self, image, position, enabled = False):
        super().__init__(image, position)
        self.speed = 5
        self.out_position = [150,15]
        self.in_position = [70,15]
        self.position = self.out_position
        self.enabled = enabled
        
    def fly_to(self,pos):
        if abs(self.position[0] - pos[0]) > 2:
            # print("flying")
            distance = math.sqrt( (pos[0] - self.position[0])**2 + (pos[1] - self.position[1])**2 )
            distance = distance if distance != 0 else 1
            dir = ((pos[0] - self.position[0])/distance,(pos[1] - self.position[1])/distance )
   
            self.position = [self.position[0] + dir[0] * self.speed, self.position[1] + dir[1] * self.speed]

    def update(self):
        if self.enabled:
            self.fly_to(self.in_position)
            
        else:
            self.fly_to(self.out_position)
            

    def render(self,display,offset=(0,0)):
        display.blit(self.image,(self.position[0] - offset[0],self.position[1] - offset[1]))



class option(panel):
    def __init__(self,image,position,handle = None):
        super().__init__(image,position)
        self.panel_surface = pygame.Surface((48,62))
        self.panel_surface.fill((255,255,255))
        self.music_slider = Slider((25,10),(30,5),0.5,0,1)
        self.sfx_slider = Slider((25,30),(30,5),0.5,0,1)
        self.handle = handle
    def update(self):
        super().update()
        mpos = [pygame.mouse.get_pos()[0]/5-self.position[0],pygame.mouse.get_pos()[1]/5-self.position[1] ]
        if self.music_slider.container_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.music_slider.move_slider(mpos)
        if self.sfx_slider.container_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.sfx_slider.move_slider(mpos)     

        setattr(self.handle,"music_volume",self.music_slider.get_value())
        setattr(self.handle,"sfx_volume",self.sfx_slider.get_value())

        # print(self.handle.music_volume,self.handle.sfx_volume)
    def render(self, display, offset=(0, 0)):
        # super().render(display, offset)
        self.panel_surface.blit(self.image,(0,0))
        self.music_slider.render(self.panel_surface)
        self.sfx_slider.render(self.panel_surface)
        display.blit(self.panel_surface,(self.position[0] - offset[0],self.position[1] - offset[1]))
        
        
class about(panel):
    def __init__(self,image,position):
        super().__init__(image,position)
        self.panel_surface = pygame.Surface((48,62))
        self.panel_surface.fill((255,255,255))
    def render(self, display, offset=(0, 0)):
        self.panel_surface.blit(self.image,(0,0))
        display.blit(self.panel_surface,(self.position[0] - offset[0],self.position[1] - offset[1]))



class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        # label
        # self.label_rect = self.text.get_rect(center = (self.pos[0], self.slider_top_pos - 15))
        
    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos
    def hover(self):
        self.hovered = True
    def render(self, surface):
        pygame.draw.rect(surface, "darkgray", self.container_rect)
        pygame.draw.rect(surface, BUTTONSTATES[self.hovered], self.button_rect)
    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val/val_range)*(self.max-self.min)+self.min
