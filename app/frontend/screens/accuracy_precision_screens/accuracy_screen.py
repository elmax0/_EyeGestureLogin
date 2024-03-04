from kivy.uix.relativelayout import RelativeLayout

from app.config import config
from app.frontend.screens import SceneScreen
from app.frontend.screens.accuracy_precision_screens.accuracy_widget import AccuracyWidget
from app.utils.recording_helper import RecordingHelper

POSITIONS = config['POSITIONS']


class AccuracyPrecisionScreen(SceneScreen, RelativeLayout):

    def __init__(self, recording_helper: RecordingHelper, end_callback, **kw):
        super().__init__(**kw)
        self._recording_helper = recording_helper
        self._end_callback = end_callback
        self.accuracy_widget = AccuracyWidget(self.end, size=self.size)
        self.add_widget(self.accuracy_widget)

    def show_point(self, pid):
        self.accuracy_widget.show_point(pid)

    def end(self):
        # self.parent.current = 'end'
        self._end_callback()

    def hide_point(self):
        self.accuracy_widget.hide_point()

    def highlight_point(self):
        self.accuracy_widget.highlight_point()

    def on_enter(self, *args):
        self._recording_helper.start('accuracy', 'precision')
        self.accuracy_widget.start()
        pass

    def on_leave(self, *args):
        # stop video
        self._recording_helper.stop()
        pass
