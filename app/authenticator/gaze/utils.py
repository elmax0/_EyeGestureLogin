import math
import numpy as np


class Gaze:
    """
    Transforms the raw Tobii-gaze-data into a gaze-object which has many attributes like:
    timestamp, x, y, ms_timestamp, etc.
    """
    TIME_KEY = 'system_time_stamp'
    L_KEY = 'left_gaze_point_on_display_area'
    R_KEY = 'right_gaze_point_on_display_area'

    def __init__(self, gaze_data):
        self._timestamp = gaze_data[self.TIME_KEY]
        self._raw_right = gaze_data[self.R_KEY]
        self._raw_left = gaze_data[self.L_KEY]
        self._gaze = create_one_single_gaze(*self._raw_left, *self._raw_right)

    def add_offset(self, offset):
        # self._gaze = (self._gaze[0] - offset[0], self._gaze[1] - offset[1]) # old code -> was wrong in x-axis
        self._gaze = (self._gaze[0] + offset[0], self._gaze[1] - offset[1])

    def print(self):
        print(f"x: {self._gaze[0]} \t y: {self._gaze[1]}")

    @property
    def has_nan(self):
        return np.isnan(self.x) or np.isnan(self.y)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def ms_timestamp(self):
        return self._timestamp / 1000

    @property
    def x(self):
        return self._gaze[0]

    @property
    def y(self):
        return self._gaze[1]

    @property
    def coords(self):
        return self.x, self.y


class Fixation:
    def __init__(self, x, y, start, end, num_gaze_points, id):
        self.x = x
        self.y = y
        self.start = start
        self.end = end
        self.num_gaze_points = num_gaze_points
        self.fix_id = id

    @classmethod
    def from_replay_coords(cls, x, y):
        return Fixation(x, y, 0, 0, 0, 0)

    @property
    def duration(self):
        return self.end - self.start

    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y

    @property
    def get_coords(self):
        return self.x, self.y

    def add_offset(self, xx, yy):
        self.x += xx
        self.y += yy

    @property
    def get_id(self):
        return self.fix_id

    @property
    def timestamp(self):
        return self.start


class Saccade:
    """
    Saccade was for old saccade-based authentication.
    So not used anymore, but for posthoc analysis it is important, so i didn't delete it
    """

    def __init__(self, source_fix: Fixation, target_fix: Fixation, last_stroke_end, s_id):
        self.source = source_fix
        self.target = target_fix
        self._dist = math.sqrt((target_fix.x - source_fix.x) ** 2 + (target_fix.y - source_fix.y) ** 2)
        self._ttl = max(self.start - last_stroke_end, 0)
        self.str_id = s_id

    @classmethod
    def from_replay_coords(cls, x1, y1, x2, y2):
        return Saccade(Fixation.from_replay_coords(x1, y1), Fixation.from_replay_coords(x2, y2), 0, 0)

    @property
    def get_id(self):
        return self.str_id

    @property
    def duration(self):
        return self.target.end - self.source.start

    @property
    def ms_dur(self):
        return self.duration / 1000000

    @property
    def num_gaze_points(self):
        return self.target.num_gaze_points + self.source.num_gaze_points

    @property
    def distance(self):
        return self._dist

    @property
    def get_coords(self):
        return self.source.get_coords, self.target.get_coords

    @property
    def start(self):
        return self.source.start

    @property
    def end(self):
        return self.target.end

    @property
    def time_gap(self):
        return self._ttl / 1000000

    @property
    def speed(self):
        return self.distance / self.duration

    @property
    def velocity(self):
        return self.distance / self.ms_dur

    def print(self):
        print(
            f"start: {self.start} \t end: {self.end} \t tgap: {self.time_gap} \n {self.source.get_id} - {self.target.get_id}")


def create_one_single_gaze(lx, ly, rx, ry):
    if lx == "nan" and rx == "nan":
        x = "nan"
    elif lx == "nan":
        x = rx
    elif rx == "nan":
        x = lx
    else:
        x = (lx + rx) / 2
    if ly == "nan" and ry == "nan":
        y = "nan"
    elif ly == "nan":
        y = ry
    elif ry == "nan":
        y = ly
    else:
        y = (ly + ry) / 2
    return x, y


def convert_coord_to_x_y(coord):
    x, y = coord
    x = x[1:]
    y = y[1:-1]
    return x, y
