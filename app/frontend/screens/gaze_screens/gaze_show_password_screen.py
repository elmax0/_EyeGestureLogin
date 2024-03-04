from kivy.clock import Clock

from app.config import config
from app.frontend.screens.screen import SceneScreen
from .gaze_password_visualisation_widget import ShowPassword

PASSWORD_LIST = config['PASSWORD_LIST']
PASSWORD_SHOW_TIME = config['PASSWORD_SHOW_TIME']


class GazeShowPasswordScreen(SceneScreen):
    """
    Shows the pattern to the user
    """

    def __init__(self, scenario_callback, **kw):
        super().__init__(**kw)
        self._scenario_callback = scenario_callback
        self._scenario = None
        self.login = None

    def on_enter(self, *args):
        # get current pattern/scenario
        self._scenario = self._scenario_callback()
        password = PASSWORD_LIST[self._scenario]
        # create login-widget to show the pattern
        self.login = ShowPassword(password=password)
        self.add_widget(self.login)
        Clock.schedule_once(self.switch_screen, PASSWORD_SHOW_TIME)

    def on_leave(self):
        self.clear_widgets()
        self.login = None
