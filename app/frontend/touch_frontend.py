from kivy import Config
from kivy.app import App
from kivy.uix.screenmanager import NoTransition

from app.authenticator.touch_authenticator import TouchAuthenticator
from app.frontend.screens import SceneScreenManager, ValidationScreen, EndScreen
from app.frontend.screens.gaze_screens import GazeStartScreen
from app.frontend.screens.touch_screens import TouchGreetingScreen, AuthenticationScreen, TouchShowPasswordScreen


class TouchFrontend(App):
    def __init__(self, recording_helper, training=False, set_size=15, drawing=False, **kwargs):
        Config.set('graphics', 'fullscreen', 'auto')
        self._training = training
        self._set_size = set_size
        self._drawing = drawing
        self._recording_helper = recording_helper
        # authenticator
        super().__init__(**kwargs)
        self.sm = SceneScreenManager(transition=NoTransition())
        self.start_screen: GazeStartScreen = None
        self.show_pw_screen: TouchShowPasswordScreen = None
        self.greeting_screen: TouchGreetingScreen = None
        self.authentication_screen: AuthenticationScreen = None
        self.validation_screen: ValidationScreen = None
        self.end_screen: EndScreen = None
        self.authenticator = TouchAuthenticator(self._recording_helper,
                                                end_authentication_callback=self.end_authentication)

    def get_scenario(self):
        return self.authenticator.get_scenario()

    def end_authentication(self):
        self.authentication_screen.switch_screen()

    def participant_confirms_password(self):
        self.authenticator.password_entry_confirmed()
        pass

    def participant_rejects_password(self):
        self.authenticator.password_entry_rejected()
        pass

    def finish_authentication_process(self):
        self.sm.switch_to(self.end_screen)
        pass

    def build(self):
        # init the screens
        self.start_screen = GazeStartScreen(name='start')
        self.show_pw_screen = TouchShowPasswordScreen(name='show_pw', scenario_callback=self.get_scenario)
        self.greeting_screen = TouchGreetingScreen(
            authenticator=self.authenticator,
            recording_helper=self._recording_helper,
            name='greeting')
        self.authentication_screen = AuthenticationScreen(
            authenticator=self.authenticator,
            scenario_callback=self.get_scenario,
            drawing=self._drawing,
            training=self._training
        )

        self.validation_screen = ValidationScreen(
            name='verification',
            accept_callback=self.participant_confirms_password,
            reject_callback=self.participant_rejects_password,
            scenario_callback=self.get_scenario,
            finish_authentication_callback=self.finish_authentication_process,
            set_size=self._set_size
        )
        # connect the screens
        self.end_screen = EndScreen(name='end')
        self.sm.add_screen(self.start_screen)
        self.sm.add_screen(self.show_pw_screen)
        self.sm.add_screen(self.greeting_screen)
        self.sm.add_screen(self.authentication_screen)
        self.sm.add_screen(self.validation_screen)
        self.sm.add_screen(self.end_screen)

        self.sm.connect(self.start_screen, self.show_pw_screen)
        self.sm.connect(self.show_pw_screen, self.greeting_screen)
        self.sm.connect(self.greeting_screen, self.authentication_screen)
        self.sm.connect(self.authentication_screen, self.validation_screen)
        self.sm.connect(self.validation_screen, self.show_pw_screen)
        return self.sm
