from kivy.clock import Clock
from kivy.graphics import Color, Ellipse

from app.authenticator.authenticator import Authenticator
from app.config import config
from app.frontend.screens.screen import SceneScreen
from app.utils import AnimationImage

IMG_PATH = config['GREETING_ARROW_PATH']
WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
AVATAR_SIZE = config['AVATAR_SIZE']
GREETING_TIME = config['GREETING_TIME']
POSITIONS = config['POSITIONS']
AOI_RADIUS = config['AOI_RADIUS']


class GreetingScreen(SceneScreen):

    def __init__(self, authenticator: Authenticator, **kw):
        super().__init__(**kw)
        self.authenticator = authenticator
        self.image: AnimationImage = None

    def on_enter(self, *args):
        # call authenticator to start
        self.authenticator.start()
        # add image
        self.image = AnimationImage(
            source=IMG_PATH,
            size_hint=(None, None),
            pos=(self.width / 2 - AVATAR_SIZE / 2, self.height / 2 - AVATAR_SIZE / 2),
            size=(AVATAR_SIZE, AVATAR_SIZE)
        )
        self.add_widget(self.image)

    def on_leave(self, *args):
        self.canvas.clear()
        self.clear_widgets()

    def call_animation(self):
        Clock.schedule_once(lambda dt: self.animate(), 0)

    def call_stop_animation(self):
        Clock.schedule_once(lambda dt: self.stop_animating(), 0)

    def animate(self):
        with self.canvas:
            Color(1, 0, 0)
            Ellipse(pos=(self.width / 2 - 2, self.height / 2 - 2), size=(4, 4))
        self.image.set_center(self.width / 2, self.height / 2)
        self.image.start_animation()

    def stop_animating(self):
        self.image.stop_animation()
