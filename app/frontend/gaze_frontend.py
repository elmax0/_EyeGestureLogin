from kivy import Config
from kivy.app import App
from kivy.uix.screenmanager import NoTransition

from app.authenticator.authenticator import Authenticator
from app.authenticator.gaze import Fixation
from app.frontend.screens import EndScreen, SceneScreenManager, InterludeScreen
from app.frontend.screens.accuracy_precision_screens import AccuracyPrecisionScreen
from app.frontend.screens.gaze_screens import AuthenticationScreen, GreetingScreen, GazeValidationScreen, \
    GazeStartScreen, GazeShowPasswordScreen


class GazeFrontend(App):
    """
       The GazeFrontend class manages the graphical user interface for gaze-based authentication.

       Args:
           recording_helper: Instance of the RecordingHelper for managing recording.
           training (bool): Flag indicating whether the frontend is in training mode.
           set_size (int): Size of the pattern set.
           drawing (bool): Flag indicating whether drawing is enabled.
           remote_control (bool): Flag indicating whether remote control is enabled.
           **kwargs: Additional keyword arguments to be passed to the App constructor.
    """

    def __init__(self,
                 recording_helper,
                 training=False,
                 set_size=15,
                 drawing=False,
                 remote_control=True,
                 **kwargs
                 ):
        Config.set('graphics', 'fullscreen', 'auto')
        self._training = training
        self._set_size = set_size
        self._drawing = drawing
        self._remote_control = remote_control
        self._recording_helper = recording_helper
        super().__init__(**kwargs)
        self.sm = SceneScreenManager(transition=NoTransition())
        self.start_screen: GazeStartScreen = None
        self.show_pw_screen: GazeShowPasswordScreen = None
        self.greeting_screen: GreetingScreen = None
        self.authentication_screen: AuthenticationScreen = None
        self.validation_screen: GazeValidationScreen = None
        self.interlude_screen: InterludeScreen = None
        self.authenticator = Authenticator(
            recording_helper=self._recording_helper,
            end_authentication_callback=self.end_authentication,
            fixation_callback=self.fixation_callback,
            offset_callback=self.switch_to_auth_screen,
            start_animation_callback=self.start_animation,
            stop_animation_callback=self.stop_animation,
        )

    def get_scenario(self):
        return self.authenticator.get_scenario()

    def end_authentication(self):
        self.authentication_screen.switch_screen()

    def fixation_callback(self, fixation: Fixation):
        self.authentication_screen.add_fixation(fixation)

    def switch_to_auth_screen(self):
        self.greeting_screen.switch_screen()

    def participant_confirms_password(self):
        self.authenticator.password_entry_confirmed()

    def participant_rejects_password(self):
        self.authenticator.password_entry_rejected()

    def start_animation(self):
        self.greeting_screen.call_animation()

    def stop_animation(self):
        self.greeting_screen.call_stop_animation()

    def finish_all_authentication_processes(self):
        # stop eye_tracker
        self.authenticator.stop_all_authentication()
        # switch to 'end_screen'
        if self._training:
            self.sm.switch_to(self.end_screen)
            return
        self.sm.switch_to(self.interlude_screen)

    def finish_accuracy_precision_process(self):
        self.sm.switch_to(self.end_screen)

    def end_application(self):
        App.get_running_app().stop()

    def build(self):
        # Init all screens
        self.start_screen = GazeStartScreen(name='start')
        self.show_pw_screen = GazeShowPasswordScreen(name='show_pw', scenario_callback=self.get_scenario)
        self.greeting_screen = GreetingScreen(name='greeting', authenticator=self.authenticator)
        self.authentication_screen = AuthenticationScreen(name='authentication', authenticator=self.authenticator)
        self.interlude_screen = InterludeScreen(name='interlude')
        self.end_screen = EndScreen(name='end')
        self.acc_prec_screen = AccuracyPrecisionScreen(name='accuracy',
                                                       recording_helper=self._recording_helper,
                                                       end_callback=self.finish_accuracy_precision_process)
        # check for remote control (instead of touch)

        self.validation_screen = GazeValidationScreen(
            name='verification',
            accept_callback=self.participant_confirms_password,
            reject_callback=self.participant_rejects_password,
            scenario_callback=self.get_scenario,
            finish_authentication_callback=self.finish_all_authentication_processes,
            set_size=self._set_size
        )
        # connect the screens
        self.sm.add_screen(self.start_screen)
        self.sm.add_screen(self.show_pw_screen)
        self.sm.add_screen(self.greeting_screen)
        self.sm.add_screen(self.authentication_screen)
        self.sm.add_screen(self.validation_screen)
        self.sm.add_screen(self.interlude_screen)
        self.sm.add_screen(self.end_screen)

        self.sm.add_screen(self.acc_prec_screen)
        self.sm.connect(self.interlude_screen, self.acc_prec_screen)

        self.sm.connect(self.start_screen, self.show_pw_screen)
        self.sm.connect(self.show_pw_screen, self.greeting_screen)
        self.sm.connect(self.greeting_screen, self.authentication_screen)
        self.sm.connect(self.authentication_screen, self.validation_screen)
        self.sm.connect(self.validation_screen, self.show_pw_screen)
        return self.sm
