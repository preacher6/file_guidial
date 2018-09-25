import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Dial:
    """Clase que permite crear el dial"""
    def __init__(self, image, flecha, size, origen, radio, ide=0):
        self.image = pygame.image.load(image)
        self.flecha = pygame.image.load(flecha)
        self.size = size
        self.center = origen
        self.radio = radio
        #self.labels = ['-10', '0', '10']
        #self.angles = [215, 90, 325]
        self.ide = ide
        self.position = (self.center[0]-self.size[0]/2, self.center[1]-self.size[1]/2)
        self.surface_button = pygame.Surface(self.size)
        self.surface_button.fill(WHITE)
        self.surface_button.blit(self.image, (0, 0))
        self.font = pygame.font.SysFont('Arial', 16, bold=True)

    def draw(self, screen):
        """Dibujar dial y etiquetas"""
        screen.blit(self.surface_button, self.position)
        screen.blit(self.font.render('0', True, BLACK), (227, 10))
        """for label, angle in zip(self.labels, self.angles):
            x_pos = (self.radio) * math.cos(math.radians(angle))
            y_pos = -(self.radio+15) * math.sin(math.radians(angle))
            screen.blit(self.font.render(label, True, BLACK), (x_pos+self.center[0]-4,
                                                               y_pos+self.center[1]))"""

