from kivy.graphics import Ellipse, Color, Line
from kivy.uix.widget import Widget

CROSSHAIR_SIZE = 15


class ActivationPoint(Widget):
    def __init__(self, pid, radius=50, position=(50, 50), **kwargs):
        super().__init__(**kwargs)
        self.id = pid
        self.radius = radius
        self.position = position
        self.size = (radius, radius)
        self.size2 = (radius / 10, radius / 10)
        self._highlighted = False
        self.pos = (self.position[0] - self.size[0] / 2.0, self.position[1] - self.size[1] / 2.0)
        self.pos2 = (self.position[0] - self.size2[0] / 2.0, self.position[1] - self.size2[1] / 2.0)
        self.size_hint = None, None
        self.draw()

    def get_pid(self):
        return self.id

    def set_pos(self, pos):
        self.position = pos
        self.pos = (self.position[0] - self.size[0] / 2.0, self.position[1] - self.size[1] / 2.0)
        self.pos2 = (self.position[0] - self.size2[0] / 2.0, self.position[1] - self.size2[1] / 2.0)

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            if self._highlighted:
                Color(1, 0, 1)
            else:
                Color(0, 1, 0)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 1, 1)
            Ellipse(pos=self.pos2, size=self.size2)
            Line(points=[self.position[0] - CROSSHAIR_SIZE, self.position[1],
                         self.position[0] + CROSSHAIR_SIZE, self.position[1]])
            Line(points=[self.position[0], self.position[1] - CROSSHAIR_SIZE,
                         self.position[0], self.position[1] + CROSSHAIR_SIZE])

    def print(self):
        print(f"pos: {self.pos}, position: {self.position}, size:{self.size}")

    def highlight(self):
        self._highlighted = True
        self.draw()

    def stop_highlight(self):
        self._highlighted = False
        self.draw()

    @property
    def offset_position(self):
        return self.position[0] - self.size[0] / 2.0, self.position[1] - self.size[1] / 2.0

    @property
    def t_pos(self):
        return self.position[0] * self.get_root_window().width, self.position[1] * self.get_root_window().height
