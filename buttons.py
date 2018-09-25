import pygame

BLACK = (255, 255, 255)


class Dial:
    def __init__(self, image, flecha, size, origen, radio, ide=0):
        self.image = pygame.image.load(image)
        self.flecha = pygame.image.load(flecha)
        self.size = size
        self.center = origen
        self.radio = radio
        self.ide = ide
        self.position = (self.center[0]-self.size[0]/2, self.center[1]-self.size[1]/2)
        self.surface_button = pygame.Surface(self.size)
        self.surface_button.fill(BLACK)
        self.surface_button.blit(self.image, (0, 0))

    def draw(self, screen):
        screen.blit(self.surface_button, self.position)
