from app.authenticator.gaze import Fixation, FixationHandler


class GazeHandler:
    """
   The GazeHandler class manages the processing of gaze data, fixation detection, and animation control.

   Args:
       fixation_callback: Callback function for detected fixations.
       start_animation_callback: Callback function to start animation.
       stop_animation_callback: Callback function to stop animation.
       start_authentication_callback: Callback function to start authentication.
       offset_callback: Callback function for calculated offset.
       start_offset_calculation_callback: Callback function to start offset calculation.
       offset_calculation_failed_callback: Callback function for failed offset calculation.
       eyes_recognized_callback: Callback function for recognized eyes.
    """

    def __init__(self,
                 fixation_callback,
                 start_animation_callback,
                 stop_animation_callback,
                 start_authentication_callback,
                 offset_callback,
                 start_offset_calculation_callback,
                 offset_calculation_failed_callback,
                 eyes_recognized_callback):
        self._fixation_callback = fixation_callback
        self._start_animation = start_animation_callback
        self._stop_animation = stop_animation_callback
        self._offset_callback = offset_callback
        self._start_offset_calculation_callback = start_offset_calculation_callback
        self._offset_calculation_failed_callback = offset_calculation_failed_callback
        self._eyes_recognized_callback = eyes_recognized_callback
        self._start_authentication = start_authentication_callback
        self._fixation_handler = FixationHandler(self._on_fixation, self._on_eyes_detected, self._on_offset,
                                                 self._on_start_offset_calculation,
                                                 self._offset_calculation_failed_callback, self._start_animation,
                                                 self._stop_animation)
        self._active = False

        pass

    def start(self):
        self._active = True
        self._fixation_handler.start()

    def start_authentication(self):
        self._fixation_handler.start_authentication()
        pass

    def stop_all_authentication(self):
        self._fixation_handler.stop_eye_tracker()

    def stop(self):
        self._active = False
        self._fixation_handler.end()

    def _on_eyes_detected(self, timestamp):
        self._eyes_recognized_callback(timestamp)

    def _on_offset(self, timestamp, offset):
        self._offset_callback(timestamp, offset)

    def _on_fixation(self, aoi_hit, fixation: Fixation):
        self._fixation_callback(aoi_hit, fixation)

    def _on_start_offset_calculation(self, timestamp):
        self._start_offset_calculation_callback(timestamp)

    def _on_offset_calculation_failed(self, timestamp):
        self._offset_calculation_failed_callback(timestamp)

    def get_raw_data(self):
        return self._fixation_handler.get_raw_data()
