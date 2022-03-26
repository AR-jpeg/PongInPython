import pygame

pygame.init()
pygame.mixer.init()

PADDLE_HIT_SOUND = pygame.mixer.Sound("assets/paddle_hit.wav")
HIT_WALL_SOUND = pygame.mixer.Sound("assets/hit_wall.wav")