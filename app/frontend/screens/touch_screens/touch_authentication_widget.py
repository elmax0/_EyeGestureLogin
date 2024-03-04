import time

from kivy.graphics import Color, Line

from app.authenticator.touch_authenticator import TouchAuthenticator
from app.frontend.screens.touch_screens.login_screen import LoginScreen
from app.utils import Event


class TouchAuthenticationWidget(LoginScreen):

    def __init__(self, authenticator: TouchAuthenticator,
                 end_callback,
                 aoi_activated_callback,
                 drawing=False,
                 training=False,
                 **kw):
        super().__init__(**kw)
        self._authenticator = authenticator
        self._end_callback = end_callback
        self._aoi_activated_callback = aoi_activated_callback
        self._drawing = drawing
        self._training = training
        self._points = []
        self.vertices = []
        self._active = False
        self._activated_points = []
        self.draw()
        self._add_event(Event.from_start_authentication())

    def _add_event(self, event: Event):
        self._authenticator.add_event(event)

    def _hits(self, touch):
        for vert in self.vertices:
            if vert.touch_collide_point(touch.x, touch.y) and vert not in self._activated_points:
                return vert
        return None

    def _evaluate(self):
        # checks if the entered pattern is correct
        result = [vec.id for vec in self._activated_points]
        if len(result) > 0 and result != self._password:
            if not self._training:
                self._add_event(Event.from_failed_authentication())
                self._end_login()
        if result == self._password:
            self._add_event(Event.from_successful_authentication())
            self._end_login()
        return result == self._password

    def _end_login(self):
        self._add_event(Event.from_end_event())
        self._lines = []
        self._activated_points = []
        self.parent.manager.current = self._next_screen

    def end(self):
        self._points = []
        self.vertices = []
        self._active = False
        self._activated_points = []
        self.clear_widgets()

    def on_touch_down(self, touch):
        self._add_event(Event.from_touch_down(touch))
        for vert in self.vertices:
            if vert.touch_collide_point(touch.x, touch.y):
                self._active = True
                if self._drawing:
                    with self.canvas:
                        Color(1, 1, 0)
                        d = 30
                        touch.ud['line_cur'] = Line(points=(touch.x, touch.y))
                self._line_start = touch.pos
                self._activated_points.append(vert)
                self._aoi_activated_callback(time.time(), vert.id)
                self._add_event(
                    Event.from_point_activated_touch(touch, vert.id, [point.id for point in self._activated_points]))

    def on_touch_move(self, touch):
        if self._active:
            target = self._hits(touch)
            if target:
                if self._drawing:
                    self._create_line(self._activated_points[-1], target)
                self._activated_points.append(target)
                self._aoi_activated_callback(time.time(),
                                             target.id)  # , [point.id for point in self._activated_points])
                self._add_event(
                    Event.from_point_activated_touch(touch, target.id, [point.id for point in self._activated_points]))
                self._line_start = target.get_center()
            else:
                if self._drawing:
                    with self.canvas:
                        touch.ud['line_cur'].points = [*self._line_start, touch.x, touch.y]

    def on_touch_up(self, touch):
        # event
        self._add_event(Event.from_touch_up(touch))
        self._authenticator.start_validating()
        if self._active:
            self._active = False
            # if not self._evaluate():
            if self._drawing:
                touch.ud['line_cur'].points = []
                with self.canvas:
                    for line in self._lines:
                        self.canvas.remove(line)
            self._lines = []
            self._activated_points = []
