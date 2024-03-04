from kivy.clock import Clock
from kivy.graphics import Ellipse, Color

from app.authenticator import Authenticator
from app.authenticator.gaze import Fixation
from app.config import config
from app.frontend.screens.screen import SceneScreen

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
POSITIONS = config['POSITIONS']
AOI_RADIUS = config['AOI_RADIUS']


class AuthenticationScreen(SceneScreen):

    def __init__(self, authenticator: Authenticator, **kw):
        super().__init__(**kw)
        self._authenticator = authenticator

    def on_enter(self, *args):
        # when this screan appears, start the authenticator
        self.canvas.clear()
        self.draw()
        self._authenticator._start_authentication_process()

    def draw(self):
        # draws the AOIs of the empty lock pattern
        with self.canvas:
            Color(0, .9, .9)
            for x, y in POSITIONS:
                tmp_x = x * self.width
                tmp_y = y * self.height
                Ellipse(pos=(tmp_x - AOI_RADIUS / 2, tmp_y - AOI_RADIUS / 2), size=(AOI_RADIUS, AOI_RADIUS))

    def add_fixation(self, fixation: Fixation):
        Clock.schedule_once(lambda dt: self._add_fixation(fixation), 0)
        pass

    def _add_fixation(self, fixation: Fixation):
        # test function to let the frontend draw fixations
        x, y = fixation.get_coords
        tobii_y = 1 - y
        tmp_x = x * self.width
        tmp_y = tobii_y * self.height
        with self.canvas:
            Color(1, 0, 0)
            Ellipse(pos=(tmp_x, tmp_y), size=(3, 3))

    def on_leave(self):
        self.canvas.clear()
        self.clear_widgets()
