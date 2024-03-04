class AOI:
    def __init__(self, aoi_id, pos, radius=.15):
        self._id = aoi_id
        self._pos = pos
        self._radius = radius
        self._x = pos[0]
        self._y = pos[1]
        self._tobii_y_coord = 1 - self._y

    def hits(self, x, y):
        x_dif = x - self._x
        y_dif = y - self._tobii_y_coord
        distance = pow(x_dif, 2) + pow(y_dif, 2)
        return distance < pow(self._radius, 2)

    @property
    def id(self):
        return self._id
