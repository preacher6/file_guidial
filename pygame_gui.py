import pygame
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
from buttons import Dial

WHITE = (255, 255, 255)

class PygameGui:
	"""Clase para creación de GUI"""
	def __init__(self):
		#super(ClassName, self).__init__() # Solo util si hago subclass
		self.clock = pygame.time.Clock()
		self.dots = list()
		self.i = 0
		self.pasos = 20
		self.grid_limit = [0, self.pasos]
		self.inicializar_pygame()

	def inicializar_pygame(self):
		pygame.init() # Inicializar pygame
		os.environ['SDL_VIDEO_CENTERED'] = '1' # Centrar GUI
		WINDOWS_SIZE = (600, 500)
		self.SCREEN = pygame.display.set_mode(WINDOWS_SIZE)

	#@staticmethod
	def draw_buttons(self):
		self.dial_button.draw(self.SCREEN)

	@staticmethod
	def draw_axis(fig):
		canvas = agg.FigureCanvasAgg(fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()
		size = canvas.get_width_height()
		surf = pygame.image.fromstring(raw_data, size, "RGB")
		return surf

	def init_plot(self):
		self.i = self.i+0.12
		self.dots.append((self.i, 0))
		x_dot = [punto[0] for punto in self.dots]
		y_dot = [punto[1] for punto in self.dots]
		if max(x_dot) >= self.grid_limit[1]:
			self.grid_limit[0]+=self.pasos/2
			self.grid_limit[1]+=self.pasos/2
			self.dots[:50] = []

		plt.cla()
		plt.grid(color='gray', linewidth=0.5, linestyle='dashed')
		plt.plot(x_dot, y_dot)
		plt.ylim([-10, 10])
		plt.xlim([self.grid_limit[0], self.grid_limit[1]])

	def run_pygame(self):
		fig = pylab.figure(figsize=[4, 4],  # Inches
                           dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           tight_layout=True)
		plt.grid(color='gray', linewidth=0.5, linestyle='dashed')
		plt.ylim([-10, 10])
		plt.xlim([0, 20])
		self.dial_button = Dial(os.path.join('pics', 'dial.png'), (60, 60), (100, 70), 'radial')
		self.ini = False
		close = False
		while not close:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					close = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					click_position = pygame.mouse.get_pos()
					self.ini = True

			self.SCREEN.fill(WHITE)
			self.draw_buttons()
			surf = self.draw_axis(fig)
			if self.ini:

				self.init_plot()
			else:
				self.counter = 0

			self.SCREEN.blit(surf, (50, 100))
			self.clock.tick(60)
			pygame.display.flip()
