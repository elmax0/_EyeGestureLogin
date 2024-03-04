from os import path

from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from app.authenticator.gaze import Fixation
from app.config import config
from app.utils import get_arrow

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
ARROW_PATH = config['ARROW_PATH4']
Config.set('graphics', 'fullscreen', 'auto')
IMG_SIZE = 150
OFFSET_PARAM = 20
POSITIONS = config['TOUCH_POSITIONS']
WIDTH_PERCENTAGE = config['WIDTH_PERCENTAGE']
HEIGHT_PERCENTAGE = config['HEIGHT_PERCENTAGE']
WIDTH_OFFSET = (1 - WIDTH_PERCENTAGE) / 2 * WIDTH
HEIGHT_OFFSET = (1 - HEIGHT_PERCENTAGE) / 2 * HEIGHT
AOI_RADIUS = config['AOI_RADIUS']


class Vertex(Widget):
    def __init__(self, v_id, radius=100, position=(50, 50), start=False, **kwargs):
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
        result = (x - cent[0]) ** 2 + (y - cent[1]) ** 2 < (self.radius * 1.2) ** 2
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
        self._fixations = []
        self.draw()

    def add_fixation(self, fixation: Fixation):
        x, y = fixation.get_coords
        x *= WIDTH
        y *= HEIGHT
        Clock.schedule_once(lambda dt: self.draw_fixation(x, y), 0)

    def draw_fixation(self, x, y):
        y = HEIGHT - y
        with self.canvas:
            # Color(1., 0, 0)
            # Add a rectangle
            Rectangle(pos=(x, y), size=(10, 10))

    def draw_saccade(self, x1, y1, x2, y2):
        x1 *= WIDTH
        x2 *= WIDTH
        y1 *= HEIGHT
        y2 *= HEIGHT
        y1 = HEIGHT - y1
        y2 = HEIGHT - y2
        with self.canvas:
            Line(bezier=(x1, y1, x2, y2))

    def add_saccade(self, s_fix: Fixation, e_fix: Fixation):
        Clock.schedule_once(lambda dt: self.draw_saccade(*s_fix.get_coords, *e_fix.get_coords), 0)
        pass

    def _create_line(self, vert1: Vertex, vert2: Vertex):
        with self.canvas:
            self._lines.append(Line(bezier=(*vert1.get_center(), *vert2.get_center())))

    def draw(self):
        with self.canvas:
            Color(1., 0, 0)
            for fix in self._fixations:
                Rectangle(pos=fix, size=(10, 10))
            for i, coord in enumerate(POSITIONS):
                position = (WIDTH * coord[0] - self.radius / 2, HEIGHT * coord[1] - self.radius / 2)
                colored = False
                self.vertices.append(Vertex(i + 1, self.radius, position, start=colored))

            for j in range(len(self.vertices)):
                self.vertices[j].draw()


class ShowPassword(LoginScreen):
    def __init__(self, *args, **kw):
        super(ShowPassword, self).__init__(*args, **kw)

    def draw(self):
        with self.canvas:
            Color(0, .9, .9)
            for i, coord in enumerate(POSITIONS):
                position = (WIDTH * coord[0] - self.radius / 2, HEIGHT * coord[1] - self.radius / 2)
                colored = False
                if (i + 1) == self._password[0]:
                    # select blue color for the start-vertex
                    colored = True
                # self.vertices.append(Vertex(i + 1, 50, position, start=colored))
                self.vertices.append(Vertex(i + 1, self.radius, position, start=colored))
            for j in range(len(self.vertices)):
                self.vertices[j].draw()
            # draw password
            Color(1, 1, 1)
            for j in range(1, len(self._password)):
                start = self._password[j - 1]
                end = self._password[j]
                self._create_line(self.vertices[start - 1], self.vertices[end - 1])
            self._create_arrow()

    def _create_arrow(self):
        arrow = get_arrow(self._password[0], self._password[1])
        arrow_path = path.join(ARROW_PATH, arrow)
        arrow_pos = self._get_arrow_pos()
        arrow_im = Image(source=arrow_path, size_hint=(None, None), keep_ratio=True,
                         pos=(arrow_pos[0] - IMG_SIZE / 2, arrow_pos[1] - IMG_SIZE / 2),
                         height=IMG_SIZE,
                         width=IMG_SIZE)
        pass

    def _get_arrow_pos(self):
        x1, y1 = self.vertices[self._password[0] - 1].get_center()
        x2, y2 = self.vertices[self._password[1] - 1].get_center()
        x_dir = x2 - x1
        y_dir = y2 - y1
        x = (x1 + x_dir / 30)
        y = (y1 + y_dir / 30)
        return x, y
