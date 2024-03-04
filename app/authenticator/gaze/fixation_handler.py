from collections import deque

import numpy as np
import tobii_research as tr

from app.authenticator.gaze.aoi import AOI
from app.config import config
from . import Fixation, Gaze

POSITIONS = config['POSITIONS']
MAX_DURATION = 500


class FixationHandler:
    def __init__(self, fixation_callback, eye_detection_callback, offset_callback, start_offset_calculation_callback,
                 offset_calculation_failed_callback, start_animation_callback, stop_animation_callback,
                 duration_threshold=100,
                 eyes_recognition_duration=config['eyes_recognition_duration']):
        """
           The FixationHandler class manages the processing of gaze data for fixation detection and offset calculation.

           Args:
               fixation_callback: Callback function for detected fixations.
               eye_detection_callback: Callback function for eye detection.
               offset_callback: Callback function for calculated offset.
               start_offset_calculation_callback: Callback function to start offset calculation.
               offset_calculation_failed_callback: Callback function for failed offset calculation.
               start_animation_callback: Callback function to start animation.
               stop_animation_callback: Callback function to stop animation.
               duration_threshold: Threshold for fixation duration. Default is 100ms.
               eyes_recognition_duration: How long eyes have to be detected before it counts as being recognized.
           """
        self._active = False
        self._duration_threshold = duration_threshold
        self.eyes_detected_callback = eye_detection_callback
        self.offset_callback = offset_callback
        self.start_offset_calculation_callback = start_offset_calculation_callback
        self.offset_calculation_failed = offset_calculation_failed_callback
        self.fixation_callback = fixation_callback
        self._recognition_duration = eyes_recognition_duration
        self._start_animation_callback = start_animation_callback
        self._stop_animation_callback = stop_animation_callback

        self._raw_data = []
        self.current = 0

        self._recognize_start_time = None
        self._eyes_recognized = False
        self._calc_offset = False

        self._start_offset_calculation_time = None
        self._offset_collection_data = deque()
        self._offset = (0., 0.)
        self._total_offset_span = config['offset_timespan']
        self._offset_collection_start_time = config['offset_collection_start_time']
        self._offset_collection_end_time = config['offset_collection_end_time']
        self._offset_trigger_radius = config['offset_trigger_radius']
        self._animation_started = False
        self.id = 0
        self._aois = []
        self._cur_aoi = None
        self._initialize_aois()

        # values from mspfix
        self._working_queue = deque()
        self._fixation_counter = 0

        self._last_fixation = None
        self._eye_tracker = None
        self._tr_running = False
        self._auth_started = False

    def start(self):
        self._active = True
        if not self._tr_running:
            self.initialize_eye_tracker()

    def _initialize_aois(self):
        for i, pos in enumerate(POSITIONS):
            tmp_aoi = AOI(i, pos)
            self._aois.append(tmp_aoi)

    def start_authentication(self):
        self._auth_started = True

    def handle_gaze(self, gaze_data):
        """
        Handles the processing of gaze-data
        First it checks if the eyes have been recognized for at least 300ms
        Then is checks if an offset has been set, if not it will handle the offset calculation
        If the authentication has started, it will check for fixations
        """
        if not self._active:
            return
        self._raw_data.append(gaze_data)
        gaze = Gaze(gaze_data)

        # step 1: check if eyes have been recognized
        if not self._eyes_recognized:
            self._check_eye_recognition(gaze)
            return
        # step 2: check if offset has been set, if not calculate offset
        if self._calc_offset:
            gaze.add_offset(self._offset)
        else:
            self._handle_offset_calculation(gaze)
        # step 3: if authentication has started -> fixation detection
        if self._auth_started:
            self.detect_fixation(gaze)

    def end(self):
        # resets the variables at the end of the authentication
        self._active = False
        self._raw_data = []
        self.current = 0
        self._working_queue = deque()
        self._fixation_counter = 0
        self.id = 0
        self._last_fixation = None
        self._recognize_start_time = None
        self._eyes_recognized = False
        self._calc_offset = False

        self._cur_aoi = None
        self._auth_started = False

        self._recognize_start_time = None

        self._start_offset_calculation_time = None
        self._offset_collection_data = deque()
        self._offset = (0., 0.)

    def get_raw_data(self):
        return self._raw_data

    def initialize_eye_tracker(self):
        found_eyetrackers = tr.find_all_eyetrackers()
        self._eye_tracker = found_eyetrackers[0]
        self._eye_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.handle_gaze, as_dictionary=True)
        self._tr_running = True

    def stop_eye_tracker(self):
        self._eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.handle_gaze)

    def _generate_fixation(self):
        norm_pos = np.array([frame.coords for frame in self._working_queue]).mean(axis=0).flatten().tolist()
        fix = Fixation(
            norm_pos[0], norm_pos[1], self._working_queue[0].timestamp, self._working_queue[-1].timestamp,
            len(self._working_queue), self._fixation_counter
        )
        self._fixation_counter += 1
        return fix

    def detect_fixation(self, gaze: Gaze):
        if gaze.has_nan:
            return
        # check if gaze is in any aoi
        # if not -> return
        aoi_hit = self._hits_aoi(gaze)
        if aoi_hit is None:
            return
        # check if hit_aoi == last_aoi
        if aoi_hit != self._cur_aoi:
            # if not -> finish fixation and set cur_aoi to hit_aoi
            old_aoi = self._cur_aoi
            self._cur_aoi = aoi_hit
            duration = self._duration(self._working_queue)
            if duration >= self._duration_threshold:
                # finish fixation
                fix = self._generate_fixation()
                self.fixation_callback(old_aoi, fix)

            # clear working queue
            self._working_queue.clear()
        # if yes -> append gaze to _working_queue
        elif len(self._working_queue) > 0:
            duration = self._duration(self._working_queue)
            if duration >= MAX_DURATION:
                fix = self._generate_fixation()
                self.fixation_callback(aoi_hit, fix)
                self._working_queue.clear()
        self._working_queue.append(gaze)

    def _hits_aoi(self, gaze: Gaze):
        for aoi in self._aois:
            if aoi.hits(gaze.x, gaze.y):
                return aoi.id
        return None

    @staticmethod
    def _calculate_dispersion(points):
        new_points = []
        for point in points:
            if not point.has_nan:
                new_points.append(point)
        norm_pos = np.array([frame.coords for frame in new_points]).mean(axis=0).flatten().tolist()
        return norm_pos

    def _check_if_gaze_in_offset_trigger_radius(self, gaze: Gaze):
        distance_from_center = (gaze.x - .5) ** 2 + (gaze.y - .5) ** 2
        return distance_from_center < self._offset_trigger_radius ** 2

    def _handle_offset_calculation(self, gaze: Gaze):
        if self._check_if_gaze_in_offset_trigger_radius(gaze):
            self._collect_and_calculate_offset_data(gaze)
        else:
            if self._animation_started:
                # stop animation & reset offset-data
                self._stop_animation_callback(gaze.timestamp)
                self._start_offset_calculation_time = None
            self._animation_started = False

    def _collect_and_calculate_offset_data(self, gaze: Gaze):
        # start offset collecting if offset_calc_time is None
        if self._start_offset_calculation_time is None:
            self._start_offset_calculation_time = gaze.ms_timestamp
            self.start_offset_calculation_callback(gaze.timestamp)
            return
        # if gaze-time is bigger than the duration of the offset calculation -> calculate offset
        if self._start_offset_calculation_time + self._offset_collection_end_time < gaze.ms_timestamp:
            self._calculate_offset(gaze)
            return
        if self._start_offset_calculation_time + self._offset_collection_start_time < gaze.ms_timestamp:
            if not self._animation_started:
                # start animation
                self._animation_started = True
                self._start_animation_callback(gaze.timestamp)
            self._offset_collection_data.append(gaze)

    def _calculate_offset(self, gaze: Gaze):
        # stop the animation and calculates the offset
        self._stop_animation_callback(gaze.timestamp)
        self._animation_started = False
        # check if data is viable for offset-calculation, if not -> redo
        if not self._offset_nan_check():
            self.offset_calculation_failed(gaze.timestamp)
            self._offset_collection_data = deque()
            self._start_offset_calculation_time = None
            return
        offset = self._calculate_dispersion(self._offset_collection_data)
        x, y = offset
        self._offset = (.5 - x, y - 0.5)
        self._calc_offset = True
        self.offset_callback(gaze.timestamp, self._offset)

    def _offset_nan_check(self):
        # checks if less than 20% of gaze-data has not nan-values
        nans = [gaze.has_nan for gaze in self._offset_collection_data]
        nan_count = 0
        for nan in nans:
            if nan:
                nan_count += 1
        if len(nans) == 0:
            return True
        else:
            result = nan_count / len(nans)
            return result <= .2

    def _check_eye_recognition(self, gaze: Gaze):
        # check if the eyes have been recognized for at least 300ms
        if gaze.has_nan and False:
            self._recognize_start_time = None
            return
        if not self._recognize_start_time:
            self._recognize_start_time = gaze.ms_timestamp
            return
        if self._recognize_start_time + self._recognition_duration < gaze.ms_timestamp:
            self._eyes_recognized = True
            self.eyes_detected_callback(gaze.timestamp)

    @staticmethod
    def _duration(frames):
        return frames[-1].ms_timestamp - frames[0].ms_timestamp
