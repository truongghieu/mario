import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zombie Destroyer")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.images = pygame.image.load("data/images/clouds/cloud_1.png")
        self.images.set_colorkey((0, 0, 0))
        self.movement = [False,False]
        self.cloud_pos = [50, 0]
        self.collider_area = [50,0,50,50]
    def run(self):
        while True:
            self.screen.fill((14, 219, 248))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False

            self.cloud_pos[1] += - self.movement[0] + self.movement[1]
           
            collider_area = pygame.Rect(self.collider_area)
            cloud_rect = pygame.Rect(self.cloud_pos, self.images.get_size())
            if cloud_rect.colliderect(collider_area):
                pygame.draw.rect(self.screen, (255, 0, 0), self.collider_area)
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), self.collider_area)
            self.screen.blit(self.images, self.cloud_pos)

            pygame.display.update()
            self.clock.tick(60)

myGame = Game()

myGame.run()
