from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from app.config import config
from app.frontend.screens.screen import SceneScreen
from app.frontend.screens.standard_screens.password_visualisation_widget import Vertex
from app.frontend.screens.standard_screens.show_password_screen import ShowPassword

""""
RATIO .7 -.3

"""

RATIO = (1, .15)

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
PASSWORD_LIST = config['PASSWORD_LIST']
WIDTH_PERCENTAGE = config['WIDTH_PERCENTAGE']
HEIGHT_PERCENTAGE = config['HEIGHT_PERCENTAGE']
WIDTH_OFFSET = (1 - WIDTH_PERCENTAGE) / 2 * WIDTH
HEIGHT_OFFSET = (1 - HEIGHT_PERCENTAGE) / 2 * HEIGHT
POSITIONS = config['TOUCH_POSITIONS']


class ValidationScreen(SceneScreen):
    def __init__(self, accept_callback, reject_callback, scenario_callback, finish_authentication_callback,
                 set_size=15, **kw):
        super().__init__(**kw)
        self._accept_callback = accept_callback
        self._reject_callback = reject_callback
        self._get_scenario = scenario_callback
        self._finish_authentication = finish_authentication_callback
        self._set_size = set_size
        self._scenario = None
        self._validation_layout: ValidationLayout = None

    def on_enter(self):
        self._scenario = self._get_scenario()
        self._validation_layout = ValidationLayout(self.accept_decision, self.reject_decision, self._scenario)
        self.add_widget(self._validation_layout)

    def accept_decision(self, event=None):
        self._accept_callback()
        if self._scenario >= self._set_size - 1:
            self._finish_authentication()
            return
        self.switch_screen()

    def reject_decision(self, Event=None):
        self._reject_callback()
        self.switch_screen()

    def on_leave(self):
        self.clear_widgets()


class ShowPasswordWidget(ShowPassword):
    def __init__(self, w_p=.8, *args, **kw):
        self._w_p = w_p
        super().__init__(*args, **kw)

    def draw(self):
        with self.canvas:
            for i, coord in enumerate(POSITIONS):
                position = self.convert_point(coord)
                colored = False
                if (i + 1) == self._password[0]:
                    colored = True
                # self.vertices.append(Vertex(i + 1, self.radius, position, start=colored))
                self.vertices.append(Vertex(i + 1, 50, position, start=colored))
            for j in range(len(self.vertices)):
                self.vertices[j].draw()
            # draw password
            self._create_arrow()
            for j in range(1, len(self._password)):
                start = self._password[j - 1]
                end = self._password[j]
                self._create_line(self.vertices[start - 1], self.vertices[end - 1])

    def convert_point(self, coord):
        w, h = self._get_position(coord)
        w -= 25
        h -= 25
        # w = .1 * WIDTH + w * .8 - self.radius/2
        # h = .2 * HEIGHT + h * .8 - self.radius/2
        return w, h

    def _get_position(self, coord):
        w, h = coord
        w *= WIDTH
        h *= HEIGHT
        # w = WIDTH_OFFSET + coord[0] * WIDTH_PERCENTAGE * WIDTH - self.radius / 2
        # h = HEIGHT_OFFSET + coord[1] * HEIGHT_PERCENTAGE * HEIGHT - self.radius / 2
        return w, h


class ValidationLayout(BoxLayout):
    def __init__(self, accept_callback, reject_callback, scenario, **kwargs):
        super().__init__(**kwargs)
        self._accept_callback = accept_callback
        self._reject_callback = reject_callback
        self._scenario = scenario
        self.orientation = 'vertical'
        self.buttons = BoxLayout(orientation='horizontal', spacing='500', padding=[100, 20, 100, 50], size_hint=RATIO)
        self.deny_btn = Button(text='deny', font_size='50sp')
        self.accept_btn = Button(text='accept', font_size='50sp')
        self.buttons.add_widget(self.deny_btn)
        self.buttons.add_widget(self.accept_btn)
        self.accept_btn.bind(on_press=self._accept_callback)
        self.deny_btn.bind(on_press=self._reject_callback)
        self.show_pw_widget = ShowPasswordWidget(password=PASSWORD_LIST[self._scenario])
        self.add_widget(self.show_pw_widget)
        self.add_widget(self.buttons)
