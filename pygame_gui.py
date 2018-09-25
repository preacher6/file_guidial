import pygame
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
from buttons import Dial

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PygameGui:
    """Clase para creación de GUI"""
    def __init__(self):
        # super(ClassName, self).__init__() # Solo util si hago subclass
        self.clock = pygame.time.Clock()
        self.dots = list()
        self.i = 0
        self.pasos = 20
        self.grid_limit = [0, self.pasos]
        self.inside_radius = False
        self.ini = False
        self.inicializar_pygame()
        self.dial_button = Dial(os.path.join('pics', 'dial_2.png'), os.path.join('pics', 'flecha.png'),
                                (80, 80), (230, 60), 32, 'radial')
        self.angle_deg = 90
        self.val_gauge = 0

    def inicializar_pygame(self):
        """Inicializar constantes y propiedades de pygame"""
        pygame.init()  # Inicializar pygame
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centrar GUI
        WINDOWS_SIZE = (480, 500)
        pygame.display.set_caption("GUI Dial")
        self.SCREEN = pygame.display.set_mode(WINDOWS_SIZE)

    # @staticmethod
    def draw_buttons(self):
        """Dibujar botón de DIAL"""
        self.dial_button.draw(self.SCREEN)

    @staticmethod
    def draw_axis(fig):
        """Dibujar el canvas que contiene el plot"""
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        return surf

    def draw_gauge(self):
        """Dibujar aguja del dial"""
        if 270 >= self.angle_deg > 225:
            self.angle_deg = 225
        elif 315 > self.angle_deg > 270:
            self.angle_deg = 315
        x_pos = (self.dial_button.radio-5)*math.cos(math.radians(self.angle_deg))
        y_pos = -(self.dial_button.radio-5)*math.sin(math.radians(self.angle_deg))
        pygame.draw.aaline(self.SCREEN, BLACK, self.dial_button.center, (x_pos+self.dial_button.center[0],
                                                                         y_pos+self.dial_button.center[1]))
        x_pos2 = (self.dial_button.radio-8) * math.cos(math.radians(self.angle_deg))
        y_pos2 = -(self.dial_button.radio-8) * math.sin(math.radians(self.angle_deg))
        nar = pygame.transform.rotate(self.dial_button.flecha, self.angle_deg)
        recta_nar = nar.get_rect(center=(x_pos2+self.dial_button.center[0],
                                         y_pos2 + self.dial_button.center[1]))
        self.SCREEN.blit(nar, recta_nar)
        new_angle = self.angle_deg+45
        if new_angle > 280:
            new_angle -= 360
        data_val = (10/270)*new_angle
        self.val_gauge = (data_val*-2)+10

    def calc_angle(self, click):
        """Calcular angulo de la aguja"""
        x2, y2 = click
        x1, y1 = self.dial_button.center
        dx = x2 - x1
        dy = y2 - y1
        angle_rads = math.atan2(-dy, dx)
        angle_rads %= 2 * math.pi
        self.angle_deg = math.degrees(angle_rads)

    def init_plot(self):
        """Plotear grafico"""
        self.i = self.i + 0.12
        self.dots.append((self.i, self.val_gauge))
        x_dot = [dot[0] for dot in self.dots]
        y_dot = [dot[1] for dot in self.dots]
        if max(x_dot) >= self.grid_limit[1]:
            self.grid_limit[0] += self.pasos / 2
            self.grid_limit[1] += self.pasos / 2
            self.dots[:50] = []
        plt.cla()
        plt.grid(color='gray', linewidth=0.5, linestyle='dashed')
        plt.plot(x_dot, y_dot)
        plt.ylim([-15, 15])
        plt.xlim([self.grid_limit[0], self.grid_limit[1]])

    def check_pos(self, click):
        """Verificar posición que desea el usuario"""
        x1, y1 = click
        x2, y2 = self.dial_button.center
        distance = math.hypot(x1-x2, y1-y2)
        if distance <= self.dial_button.radio:
            self.inside_radius = True
        else:
            self.inside_radius = False

    def run_pygame(self):
        """Ejecutar ciclo de pygame"""
        fig = pylab.figure(figsize=[4, 4],  # En pulgadas
                           dpi=100,  # 100 puntos por pulgada
                           tight_layout=True)
        plt.ylim([-15, 15])
        plt.grid(color='gray', linewidth=0.5, linestyle='dashed')
        plt.xlim([0, 20])
        self.ini = True
        close = False
        while not close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click_position = pygame.mouse.get_pos()
                    self.check_pos(click_position)

            self.SCREEN.fill(WHITE)
            self.draw_buttons()
            self.draw_gauge()
            surf = self.draw_axis(fig)
            click = pygame.mouse.get_pos()
            if self.ini:
                self.init_plot()
            if self.inside_radius and pygame.mouse.get_pressed()[0]:
                self.calc_angle(click)
            self.SCREEN.blit(surf, (35, 100))
            self.clock.tick(60)
            pygame.display.flip()
