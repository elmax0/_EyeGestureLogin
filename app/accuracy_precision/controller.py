from .accuracy_calculator import calculate_accuracy_and_precision
from .activation_module import ActivationModule
from .storage_handler import AccuracyAndPrecisionStorageHandler

POSITIONS = [[.166, .833], [0.5, 0.833], [.833, .833],
             [.166, .5], [0.5, 0.5], [.833, .5],
             [.166, .166], [0.5, 0.166], [.833, .166]]

ORDER = [4, 7, 0, 2, 6, 5, 8, 3, 1]


# TODO:
#   1) order of points
#   2) total_fail_timer = 5000


class Controller:

    def __init__(self, show_point_callback, highlight_point_callback, deactivate_point_callback, hide_point_callback,
                 end_callback):
        self._show_point_callback = show_point_callback
        self._highlight_callback = highlight_point_callback
        self._deactivate_highlight_point_callback = deactivate_point_callback
        self._hide_point_callback = hide_point_callback
        self._end_callback = end_callback
        self._activation_module = ActivationModule(self.highlight_point, self.analyze_data,
                                                   self.deactivate_highlight_point, self.show_next_point)
        self._storage_handler = AccuracyAndPrecisionStorageHandler()
        self._iter = 0
        self._gaze_data = []

    def start(self):
        # start all other components
        self._show_point_callback(self._current_point_id)
        self._activation_module.activate_point(self._current_point_id)

    def show_next_point(self):
        self._hide_point_callback()
        self._iter += 1
        if self._iter >= len(POSITIONS):
            self.end()
            pass
        else:
            self._show_point_callback(self._current_point_id)
            self._activation_module.activate_point(self._current_point_id)

    def highlight_point(self):
        self._highlight_callback()

    def deactivate_highlight_point(self):
        self._deactivate_highlight_point_callback()

    def end(self):
        # get all data
        raw_gaze_data = self._activation_module.get_raw_gaze()
        self._storage_handler.save_raw_data(raw_gaze_data)
        #   save all data
        self._end_callback()

    def analyze_data(self, raw_data):
        # get data of activated point
        point = self._current_point_position
        # give raw_data and data about act. point to acc.-module
        result = calculate_accuracy_and_precision(raw_data, point)
        # save result
        self._storage_handler.save(self._current_point_id, result, raw_data)

    @property
    def _current_point_id(self):
        return ORDER[self._iter]

    @property
    def _current_point_position(self):
        return POSITIONS[self._current_point_id]
