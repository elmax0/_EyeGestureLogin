from app.authenticator.touch_authenticator import TouchAuthenticator
from app.config import config
from app.frontend.screens import SceneScreen
from app.frontend.screens.touch_screens.touch_authentication_widget import TouchAuthenticationWidget

PASSWORD_LIST = config['PASSWORD_LIST']


class AuthenticationScreen(SceneScreen):
    def __init__(self, authenticator: TouchAuthenticator, scenario_callback, drawing=False, training=False, **kw):
        super().__init__(**kw)
        self.authenticator = authenticator
        self._scenario_callback = scenario_callback
        self._login_widget: TouchAuthenticationWidget = None
        self._drawing = drawing
        self._training = training

    def on_enter(self, *args):
        self.authenticator.start()
        password = PASSWORD_LIST[self._scenario_callback()]
        # create login-widget
        self._login_widget = TouchAuthenticationWidget(
            self.authenticator,
            self.on_end,
            self.on_aoi_activation,
            self._drawing,
            self._training,
            password=password
        )
        self.add_widget(self._login_widget)

    def on_end(self):
        self.authenticator.stop()

    def on_aoi_activation(self, timestamp, aoi):
        self.authenticator.on_aoi_activation(timestamp, aoi)

    def on_leave(self, *args):
        self._login_widget.end()
        self.clear_widgets()
