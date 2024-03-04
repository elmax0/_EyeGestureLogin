from math import pow

from app.authenticator.gaze.utils import Gaze
from app.config import config

WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']


class ActivationPoint:
    def __init__(self, pid, x, y, radius=500):
        self.pid = pid
        self.x = x
        self.y = y
        self.x_coord = x * WIDTH
        self.y_coord = y * HEIGHT
        self._tobii_y_coord = HEIGHT - self.y_coord
        self.radius = radius

    def hits(self, gaze: Gaze):
        g_x = gaze.x * WIDTH
        g_y = gaze.y * HEIGHT
        x_dif = g_x - self.x_coord
        y_dif = g_y - self._tobii_y_coord
        distance = pow(x_dif, 2) + pow(y_dif, 2)
        return distance < pow(self.radius, 2)

    def print(self):
        print(f"x: {self.x}, y: {self.y} \n"
              f"x_coord: {self.x_coord}, y_coord: {self.y_coord}")


class Result:
    def __init__(self, point: ActivationPoint, result_dict, raw_data):
        self.point = point
        self.result_dict = result_dict
        self.raw_data = raw_data
