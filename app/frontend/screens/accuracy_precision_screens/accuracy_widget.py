from kivy.clock import Clock
from kivy.uix.widget import Widget

from app.accuracy_precision.controller import Controller
from app.config import config
from app.frontend.screens.accuracy_precision_screens.activation_point import ActivationPoint

POSITIONS = config['POSITIONS']

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']


class AccuracyWidget(Widget):

    def __init__(self, end_callback, **kwargs):
        super().__init__(**kwargs)
        self._end_callback = end_callback
        self.point = None
        self.size_hint = 1, 1
        self.controller = Controller(self.trigger_show_point, self.trigger_highlight_point,
                                     self.trigger_stop_highlight_point, self.trigger_hide_point, self.end)
        self.bind(size=self.update_point_position)

    def start(self):
        self.controller.start()

    def end(self):
        self._end_callback()

    def update_point_position(self, point, value):
        if self.point:
            new_pos = self._get_position(self.point.get_pid())
            self.point.set_pos(new_pos)

    def trigger_show_point(self, pid):
        Clock.schedule_once(lambda dt: self.show_point(pid), 0)

    def trigger_hide_point(self):
        Clock.schedule_once(lambda dt: self.hide_point(), 0)

    def trigger_highlight_point(self):
        Clock.schedule_once(lambda dt: self.highlight_point(), 0)

    def trigger_stop_highlight_point(self):
        Clock.schedule_once(lambda dt: self.stop_highlight_point(), 0)

    def event_show_point(self, pid, position):
        self.point = ActivationPoint(pid=pid, position=position)
        self.add_widget(self.point)

    def show_point(self, pid):
        self.point = ActivationPoint(pid=pid, position=self._get_position(pid))
        self.add_widget(self.point)

    def _get_position(self, pid):
        normalized = POSITIONS[pid]
        x_pos = normalized[0] * self.width
        y_pos = normalized[1] * self.height
        return x_pos, y_pos

    def highlight_point(self):
        self.point.highlight()

    def stop_highlight_point(self):
        self.point.stop_highlight()
        pass

    def hide_point(self):
        self.remove_widget(self.point)
