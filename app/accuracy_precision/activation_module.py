import time

from app.accuracy_precision.gaze_handler import GazeHandler
from app.accuracy_precision.utils import ActivationPoint
from app.authenticator.gaze.utils import Gaze

POSITIONS = [[.166, .833], [0.5, 0.833], [.833, .833],
             [.166, .5], [0.5, 0.5], [.833, .5],
             [.166, .166], [0.5, 0.166], [.833, .166]]

ACTIVATION_TIME = 500
RECORDING_DURATION = 1000
MAX_ACTIVATION_DURATION = 5000
COOLDOWN_DURATION = 250


class ActivationModule:
    test_start = None

    def __init__(self, highlight_point_callback, calculate_acc_prec_callback,
                 deactivate_highlight_callback, point_completed_callback):
        self._highlight_point_callback = highlight_point_callback
        self._calculate_acc_prec_callback = calculate_acc_prec_callback
        self._deactivate_highlight_callback = deactivate_highlight_callback
        self._point_completed_callback = point_completed_callback
        self._activated_point = None
        self._activation_points = []
        self._gaze_handler = GazeHandler(self.handle_gaze)
        self._active = False
        self._idle = False
        self._await_activation = False
        self._collecting = False
        self._on_cooldown = False
        self._start_time = None
        self._activation_start_time = None
        self._collection_start_time = None
        self._point_start_time = None
        self._cooldown_start_time = None
        self._gaze_data = []
        self._raw_gaze_data = []
        self._create_activation_points()

    def _create_activation_points(self):
        for i, coord in enumerate(POSITIONS):
            tmp_point = ActivationPoint(i, *coord)
            self._activation_points.append(tmp_point)

    def activate_point(self, p_id):
        self._activated_point = self._activation_points[p_id]
        self._active = True

        self._idle = True

    def end(self):
        self._active = False
        self._await_activation = False
        self._collecting = False
        self._idle = False
        self._on_cooldown = False
        self._start_time = None
        self._activation_start_time = None
        self._collection_start_time = None
        self._cooldown_start_time = None
        self._gaze_data = []
        self._point_completed_callback()

    def get_raw_gaze(self):
        return self._raw_gaze_data

    def handle_gaze(self, raw_gaze):
        self._raw_gaze_data.append(raw_gaze)
        if not self._active:
            return
        gaze = Gaze(raw_gaze)
        if self._idle:
            if not self._start_time:
                self._start_time = gaze.ms_timestamp
            self._check_for_activation_start(gaze)
        elif self._await_activation:
            self._check_for_start_collection(gaze)
        elif self._collecting:
            self._gaze_data.append(raw_gaze)
            self._checking_for_end_collection(gaze)
        elif self._on_cooldown:
            self._checking_for_cooldown_to_end(gaze)
        else:
            print("never should land here ??")
            raise Exception('never should land here')

    def _check_for_activation_start(self, gaze):
        if self.is_gaze_in_point_radius(gaze):
            self._activation_start_time = gaze.ms_timestamp
            self.test_start = time.time()
            self._await_activation = True
            self._idle = False
        else:
            if gaze.ms_timestamp - self._start_time > MAX_ACTIVATION_DURATION:
                self.end()

    def _check_for_start_collection(self, gaze):
        if self.is_gaze_in_point_radius(gaze):
            # check for time difference
            # if duration higher than activation-time -> set to collecting
            if gaze.ms_timestamp - self._activation_start_time > ACTIVATION_TIME:
                self._collecting = True
                self._await_activation = False
                self._collection_start_time = gaze.ms_timestamp
                self._highlight_point_callback()
        else:
            if gaze.ms_timestamp - self._start_time > MAX_ACTIVATION_DURATION:
                self.end()
            else:
                self._reset()

    def _checking_for_end_collection(self, gaze: Gaze):
        if gaze.ms_timestamp - self._collection_start_time > RECORDING_DURATION:
            if self.is_gaze_in_point_radius(gaze):
                self._calculate_acc_prec_callback(self._gaze_data)
                self._collecting = False
                self._on_cooldown = True
                self._cooldown_start_time = gaze.ms_timestamp
            else:
                self._data_collection_failed()

    def _checking_for_cooldown_to_end(self, gaze: Gaze):
        if gaze.ms_timestamp - self._cooldown_start_time > COOLDOWN_DURATION:
            self.end()

    def _reset(self):
        self._idle = True
        self._await_activation = False
        self._collecting = False
        self._on_cooldown = False
        self._activation_start_time = None
        self._collection_start_time = None
        self._cooldown_start_time = None
        self._gaze_data = []

    def _data_collection_failed(self):
        # tell controller to deactivate point
        self._deactivate_highlight_callback()
        # reset everything
        self._start_time = None
        self._reset()

    def is_gaze_in_point_radius(self, gaze):
        return self._activated_point.hits(gaze)
