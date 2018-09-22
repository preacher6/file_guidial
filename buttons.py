import pygame

BLACK = (0, 0, 0)

class Dial:
	def __init__(self, image, size, origen, ide=0):
		self.image = pygame.image.load(image)
		self.size = size
		self.center = origen
		self.ide = ide
		self.position = (self.center[0]-self.size[0], self.center[1]-self.size[1])
		self.surface_button = pygame.Surface((self.size))
		self.surface_button.fill(BLACK)
		self.surface_button.blit(self.image, (0, 0))

	def draw(self, screen):
		screen.blit(self.surface_button, self.position)
