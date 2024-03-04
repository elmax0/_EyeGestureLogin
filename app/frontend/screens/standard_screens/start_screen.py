from kivy.clock import Clock

from app.config import config
from app.frontend.screens.screen import SceneScreen

INTRO_TIME = config['INTRO_TIME']


class StartScreen(SceneScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        background_color = (1, 1, 1, 0)

    def on_enter(self, *args):
        Clock.schedule_once(self.switch_screen, INTRO_TIME)
