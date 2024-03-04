from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget

from app.config import config

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
ARROW_PATH = config['ARROW_PATH']
Config.set('graphics', 'fullscreen', 'auto')
IMG_SIZE = 150
OFFSET_PARAM = 20
POSITIONS = config['TOUCH_POSITIONS']


class Vertex(Widget):
    def __init__(self, v_id, radius=50, position=(50, 50), start=False, **kwargs):
        super(Vertex, self).__init__(**kwargs)
        self.id = v_id
        self.position = position
        self.radius = radius
        self._start = start
        self.size = (radius, radius)
        self.pos = position  # need to set the `pos` as `collide_point` uses it

    def get_center(self):
        return self.pos[0] + self.radius / 2, self.pos[1] + self.radius / 2

    def touch_collide_point(self, x, y):
        cent = self.get_center()
        result = (x - cent[0]) ** 2 + (y - cent[1]) ** 2 < (self.radius * 1.6) ** 2
        return result

    def draw(self):
        with self.canvas:
            if self._start:
                Color(0, 1, 0)
            else:
                Color(1., 0, 0)
            Ellipse(pos=self.position, size=self.size)


class LoginScreen(Widget):
    def __init__(self, radius=50, password=None, **kwargs):
        super().__init__()
        if password is None:
            password = [1, 2, 4, 5]
        self.radius = radius
        self._password = password
        self.vertices = []
        self._lines = []
        self._line_start = None
        self.draw()

    def _create_line(self, vert1: Vertex, vert2: Vertex):
        with self.canvas:
            self._lines.append(Line(bezier=(*vert1.get_center(), *vert2.get_center())))

    def draw(self):
        with self.canvas:
            Color(1., 0, 0)
            for i, coord in enumerate(POSITIONS):
                position = (WIDTH * coord[0] - self.radius / 2, HEIGHT * coord[1] - self.radius / 2)
                colored = False
                self.vertices.append(Vertex(i + 1, self.radius, position, start=colored))

            for j in range(len(self.vertices)):
                self.vertices[j].draw()
