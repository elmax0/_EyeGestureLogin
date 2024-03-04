from time import time

from app.authenticator.gaze.utils import Fixation, Saccade

EVENT_TYPES = ['Fixation', 'Stroke', 'Eyes_recognized', 'Password_entry', 'Offset']

EVENT_COLUMNS = ['Local_time', 'Timestamp', 'Event', 'X', 'Y', 'END_X', 'END_Y', 'Duration', 'Password_entry',
                 'X_OFFSET', 'Y_OFFSET']


class Event:
    def __init__(self, timestamp=None, event_type='', x=None, y=None, end_x=None, end_y=None,
                 duration=None, password=None, x_offset=None, y_offset=None):
        self._local_time = time()
        self._timestamp = timestamp
        self._type = event_type
        self._x = x
        self._y = y
        self._end_x = end_x
        self._end_y = end_y
        self._duration = duration
        self._password = password
        self._x_offset = x_offset
        self._y_offset = y_offset

    @classmethod
    def from_fixation(cls, fixation: Fixation):
        return Event(fixation.start, 'Fixation', x=fixation.x, y=fixation.y, duration=fixation.duration)

    @classmethod
    def from_saccade(cls, saccade: Saccade):
        x1, y1 = saccade.get_coords[0]
        x2, y2 = saccade.get_coords[1]
        return Event(saccade.start, 'Stroke', x=x1, y=y1, end_x=x2, end_y=y2, duration=saccade.duration)

    @classmethod
    def from_password(cls, timestamp, password):
        return Event(timestamp, 'Password', password=password)

    @classmethod
    def from_start_offset_calculation(cls, timestamp):
        return Event(timestamp, 'Start offset calculation')

    @classmethod
    def from_offset(cls, timestamp, offset):
        x = offset[0]
        y = offset[1]
        return Event(timestamp, 'Offset calculated', x_offset=x, y_offset=y)

    @classmethod
    def from_offset_calculation_failed(cls, timestamp):
        return Event(timestamp, 'Offset calculation failed')

    @classmethod
    def from_eyes_detected(cls, timestamp):
        return Event(timestamp, 'Eyes_detected')

    @classmethod
    def from_password_recognized(cls, timestamp):
        return Event(timestamp, 'Password_recognized')

    @classmethod
    def from_start_event(cls):
        return Event(None, 'Start')

    @classmethod
    def from_end_event(cls):
        return Event(None, 'End')

    @classmethod
    def from_timeout(cls):
        return Event(None, 'Timeout')

    @classmethod
    def from_start_authentication(cls):
        return Event(None, 'Authentication_started')

    @classmethod
    def from_touch_down(cls, touch):
        return Event(None, 'Touch_down', touch.x, touch.y)

    @classmethod
    def from_touch_up(cls, touch):
        return Event(None, 'Touch_up', touch.x, touch.y)

    @classmethod
    def from_start_animation(cls, timestamp):
        return Event(timestamp, 'Start_offset_animation')

    @classmethod
    def from_stop_animation(cls, timestamp):
        return Event(timestamp, 'Stop_offset_animation')

    @classmethod
    def from_failed_authentication(cls, timestamp=None):
        return Event(timestamp, 'Failed Authentication')

    @classmethod
    def from_start_recording(cls, timestamp=None):
        return Event(timestamp, 'Start video recording')

    @classmethod
    def from_stop_recording(cls, timestamp=None):
        return Event(timestamp, 'Stop video recording')

    @classmethod
    def from_successful_authentication(cls, timestamp=None):
        return Event(timestamp, 'Successful Authentication')

    @classmethod
    def from_point_activated_touch(cls, touch, point, password):
        return Event(None, f"Point {point} activated", touch.x, touch.y, password=password)

    def to_row(self):
        return [self._local_time, self._timestamp, self._type, self._x, self._y, self._end_x, self._end_y,
                self._duration, self._password,
                self._x_offset, self._y_offset]
