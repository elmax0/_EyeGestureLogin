from kivy.uix.image import Image

from app.authenticator.touch_authenticator import TouchAuthenticator
from app.config import config
from app.frontend.screens.screen import SceneScreen
from app.utils import Event
from app.utils.recording_helper import RecordingHelper

# from app.utils import AnimationImage

IMG_PATH = config['GREETING_ARROW_PATH']
GREETING_DUR = config['GREETING_TIME']
WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
AVATAR_SIZE = config['AVATAR_SIZE']
GREETING_TIME = config['GREETING_TIME']
POSITIONS = config['POSITIONS']
AOI_RADIUS = config['AOI_RADIUS']


class TouchGreetingScreen(SceneScreen):
    def __init__(self, authenticator: TouchAuthenticator, recording_helper: RecordingHelper, **kw):
        super().__init__(**kw)
        self._authenticator = authenticator
        self._recording_helper = recording_helper
        self.image: Image = None

    def on_enter(self, *args):
        self._recording_helper.start(self._authenticator.scenario, self._authenticator.attempt)
        self._authenticator.add_event(Event.from_start_event())
        # add image
        self.image = Image(
            source=IMG_PATH,
            size_hint=(None, None),
            pos=(self.width / 2 - AVATAR_SIZE / 2, self.height / 2 - AVATAR_SIZE / 2),
            size=(AVATAR_SIZE, AVATAR_SIZE)
        )
        self.add_widget(self.image)

    def on_touch_down(self, touch):
        self.switch_screen()

    def on_leave(self, *args):
        self.canvas.clear()
        self.clear_widgets()
