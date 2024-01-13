import sys
import pygame
import random

from scripts.system.utils import load_image, load_images,Animation
from scripts.system.entities import object,zombie,hammer
from scripts.clouds import Clouds
from scripts.zombie_manager import zombie_manager
from scripts.boss_manager import boss_manager
from scripts.system.text import generate_font,show_text
from scripts.system.sound import load_snd

# boss
from scripts.boss.greenskin import greenskin



font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}

class Game:
    def __init__(self):
        # set up for pygame
        pygame.init()
        pygame.display.set_caption('Zombie Killer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.font_1 = generate_font('data/fonts/small_font.png',font_dat,5,8,(185,57,57))
        self.font_2 = generate_font('data/fonts/small_font.png',font_dat,5,8,(51,34,40))
        # Variables
        # music 
        pygame.mixer.music.load('data/main.wav')
        self.hit_clip = load_snd('hit')
        # ---------------
        self.last_mouse_pos = [0, 0]
        self.timer = 0
        self.scrore = 0
        self.assets = {

            'background': load_image('background.png'),
            'gameplay_base' :load_image('base.png'),
            'cell': load_image('cells/cell_2.png'),
            'score_window' : load_image('score_window.png'),
            'clouds': load_images('clouds'),
            'hammer': Animation(load_images('hammer'), 5, False),
            'zombie': load_images('zombies'),
            'boss_0' : Animation(load_images('entities/boss_0'),30,True),
        }

        # Manger
        self.zombie_manager_s = zombie_manager(zombie(Animation(self.assets['zombie'], 50,loop=False),[0,0],False), zombie_count=5, zombie_spawn_time=50)
        self.boss_manaer_s = boss_manager(False)
        self.boss_manaer_s.add_boss(greenskin(self.assets['boss_0'], (100,50),False))



        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.scroll = [0, 0]
        self.base = object(self.assets['gameplay_base'], (35, 30))
        self.score_window = object(self.assets['score_window'], (0, 0))
        self.cells = []
        for spawn in self.zombie_manager_s.spawn_positions:
            self.cells.append(object(self.assets['cell'], spawn))

        self.my_hammer = hammer(self.assets['hammer'], (50, 50))
    
    def run(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.hit_clip.set_volume(0.5)

        # self.boss_manaer_s.enable = True
        # self.boss_manaer_s.wake_up_boss(0)

        while True:
            self.timer += 1
                
            self.display.blit(self.assets['background'], (0, 0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.base.render(self.display, offset=render_scroll)
            self.base.update()
            self.score_window.render(self.display, offset=render_scroll)
            self.score_window.update()

            show_text("Score : "+str(self.scrore) ,10,10 , 1,185,self.font_2,self.display)

            for cell in self.cells:
                cell.render(self.display, offset=render_scroll)
                cell.update()

            self.zombie_manager_s.update()
            self.zombie_manager_s.render(self.display,offset=render_scroll)  

            if self.boss_manaer_s.enable:
                self.zombie_manager_s.enable = False
                
                self.boss_manaer_s.update()
                self.boss_manaer_s.render(self.display,offset=render_scroll)

                self.my_hammer.render(self.display, offset=[-50,20])
                self.my_hammer.update()
            else:
                self.my_hammer.render(self.display, offset=[-20,20])
                self.my_hammer.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # get mouse position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.last_mouse_pos = pygame.mouse.get_pos()
                    # self.last_mouse_pos = self.last_mouse_pos / self.display.get_size() * self.screen.get_size()
                    # convert tuble to list
                    self.last_mouse_pos = list(self.last_mouse_pos)
                    # convert to surface position
                    self.last_mouse_pos = [self.last_mouse_pos[0] / self.screen.get_size()[0] * self.display.get_size()[0],self.last_mouse_pos[1] / self.screen.get_size()[1] * self.display.get_size()[1]]
                    
                    if self.boss_manaer_s.enable:
                        for t_boss in self.boss_manaer_s.bosses:
                            print(t_boss.check_mouse_collision(self.last_mouse_pos))
                            if t_boss.check_mouse_collision(self.last_mouse_pos):
                                self.my_hammer.position = t_boss.position
                                self.my_hammer.enable = True
                                t_boss.take_damage(self.my_hammer.dame)
                                self.scrore += self.my_hammer.dame
                                self.hit_clip.play()
                                break
                    else:
                        for zombie in self.zombie_manager_s.zombies:
                            if zombie.check_mouse_collision(self.last_mouse_pos):
                                # print(zombie.position)
                                self.my_hammer.position = zombie.position
                                self.my_hammer.enable = True
                                zombie.enable = False
                                # print("collision")
                                self.scrore += 2
                                self.hit_clip.play()
                                break
                    self.scrore -= 1
                if event.type == pygame.MOUSEBUTTONUP:
                    self.last_mouse_pos = [0,0]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.zombie_manager_s.enable = False
                    if event.key == pygame.K_RIGHT:
                        self.zombie_manager_s.enable = True
                    # check if mouse position is over the button
                # if event.type == pygame.MOUSEBUTTONUP:
                #     self.last_mouse_pos = [0,0]
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)



Game().run()