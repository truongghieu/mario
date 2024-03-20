import pygame
def load_snd(name):
    return pygame.mixer.Sound('data/sfx/' + name + '.wav')

def load_kill(name):
    return pygame.mixer.Sound('data/sfx/kill/' + name +'.WAV')