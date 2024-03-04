from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from app.config import config
from app.frontend.screens.gaze_screens.gaze_show_password_screen import ShowPassword
from app.frontend.screens.screen import SceneScreen
from app.frontend.screens.standard_screens.password_visualisation_widget import Vertex

RATIO = (1, .15)
WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
PASSWORD_LIST = config['PASSWORD_LIST']
WIDTH_PERCENTAGE = config['WIDTH_PERCENTAGE']
HEIGHT_PERCENTAGE = config['HEIGHT_PERCENTAGE']
WIDTH_OFFSET = (1 - WIDTH_PERCENTAGE) / 2 * WIDTH
HEIGHT_OFFSET = (1 - HEIGHT_PERCENTAGE) / 2 * HEIGHT
POSITIONS = config['POSITIONS']
ARROW_PATH = config['ARROW_PATH3']
AOI_RADIUS = config['AOI_RADIUS']


class GazeValidationScreen(SceneScreen):
    """ Screen which lets the user accept or deny their pattern entry"""

    def __init__(self, accept_callback, reject_callback, scenario_callback, finish_authentication_callback,
                 set_size=15, **kw):
        super().__init__(**kw)
        self._accept_callback = accept_callback
        self._reject_callback = reject_callback
        self._get_scenario = scenario_callback
        self._finish_authentication = finish_authentication_callback
        self._set_size = set_size
        self._scenario = None
        self._active = False
        self._validation_layout: ValidationLayout = None
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, *args):
        # checks whether the participant accepts or denies the entry
        if self._active:
            if args[1] == 281:
                self.accept_decision(*args)
            elif args[1] == 280:
                self.reject_decision(*args)

    def on_enter(self):
        self._active = True
        self._scenario = self._get_scenario()
        self._validation_layout = ValidationLayout(self._scenario)
        self.add_widget(self._validation_layout)

    def accept_decision(self, *args):
        self._accept_callback()
        if self._scenario >= self._set_size - 1:
            self._finish_authentication()
            return
        self.switch_screen()

    def reject_decision(self, *args):
        self._reject_callback()
        self.switch_screen()

    def on_leave(self):
        self._active = False
        self.clear_widgets()


class ShowPasswordWidget(ShowPassword):
    def __init__(self, w_p=.8, *args, **kw):
        self._w_p = w_p
        super().__init__(*args, **kw)

    def draw(self):
        with self.canvas:
            Color(0, .9, .9)
            # draw the points on the canvas and color points that belong to the pattern
            for i, coord in enumerate(POSITIONS):
                position = self.convert_point(coord)
                colored = False
                if (i + 1) == self._password[0]:
                    colored = True
                self.vertices.append(Vertex(i + 1, AOI_RADIUS, position, start=colored))
            for j in range(len(self.vertices)):
                self.vertices[j].draw()
            Color(1, 1, 1)
            # draw the lines of the pattern
            for j in range(1, len(self._password)):
                start = self._password[j - 1]
                end = self._password[j]
                self._create_line(self.vertices[start - 1], self.vertices[end - 1])
            self._create_arrow()

    def convert_point(self, coord):
        """ Returns coordinates with offset for the center of the point """
        w, h = self._get_position(coord)
        w -= AOI_RADIUS / 2
        h -= AOI_RADIUS / 2
        return w, h

    def _get_position(self, coord):
        """ Returns coordinates for the screen """
        w, h = coord
        w *= WIDTH
        h *= HEIGHT
        return w, h


class ValidationLayout(BoxLayout):
    def __init__(self, scenario, **kwargs):
        super().__init__(**kwargs)
        self._scenario = scenario
        self.orientation = 'vertical'
        # self.buttons = BoxLayout(orientation='horizontal', spacing='500', padding=[100, 0, 100, 100], size_hint=RATIO)
        self.buttons = BoxLayout(orientation='horizontal', spacing='500', padding=[100, 20, 100, 50], size_hint=RATIO)
        self.deny_btn = Button(text='< deny', font_size='70sp')
        self.accept_btn = Button(text='accept >', font_size='70sp')
        self.buttons.add_widget(self.deny_btn)
        self.buttons.add_widget(self.accept_btn)
        self.show_pw_widget = ShowPasswordWidget(password=PASSWORD_LIST[self._scenario])
        self.add_widget(self.show_pw_widget)
        self.add_widget(self.buttons)
