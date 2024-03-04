import tobii_research as tr


class GazeHandler:

    def __init__(self, gaze_callback):
        self._gaze_callback = gaze_callback

        found_eyetrackers = tr.find_all_eyetrackers()
        self._eye_tracker = found_eyetrackers[0]
        self._eye_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.handle_gaze, as_dictionary=True)
        self._tr_running = True

    def handle_gaze(self, gaze_data):
        self._gaze_callback(gaze_data)
