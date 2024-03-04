from app.authenticator.gaze import Fixation


def check_skippable(source, dest):
    """
        Check if skipping between two AOIs (Areas of Interest) is allowed and return the intermediary AOI if skippable.
        Args:
            source (int): The source AOI.
            dest (int): The destination AOI.

        Returns: int or None: The intermediary AOI if skipping is allowed, otherwise None.
        """
    return skippable_dict.get(source).get(dest, None)


class Validator:
    """
        The Validator class handles the validation of gaze-based authentication patterns.

        Args:
            password_entry_callback: Callback function for valid password entry events.
            accept_password_callback: Callback function for successful authentication.
            reject_password_callback: Callback function for failed authentication attempts.
            password (list): The correct sequence of AOIs for authentication.
            points_not_skippable (bool, optional): Whether intermediate points should not be skipped. Default is True.
        """

    def __init__(self, password_entry_callback, accept_password_callback,
                 reject_password_callback, password, points_not_skippable=True):
        self._password_entry_callback = password_entry_callback
        self._accept_password_callback = accept_password_callback
        self._reject_password_callback = reject_password_callback
        self._password = password
        self._points_not_skippable = points_not_skippable
        self._buffer = []
        self._cur_time = None

    def add_fixation(self, aoi_id, fixation: Fixation):
        aoi_id += 1  # password starts from 1 not from 0 -> incr. aoi_id
        self._cur_time = fixation.end
        if len(self._buffer) == 0:
            # first fixation should always be at center (5), so if password doesnt start with 5 -> ignore first entry
            if not (self._password[0] != 5 and aoi_id == 5):
                self._buffer.append(aoi_id)
                self._password_entry_callback(self._cur_time, aoi_id)
            return
        # add aoi_id as new password entry
        if self._buffer[-1] != aoi_id:
            # check if a point was skipped by the user
            if self._points_not_skippable:
                skipped = check_skippable(self._buffer[-1], aoi_id)
                if skipped is not None:
                    self._buffer.append(skipped)
                    self._password_entry_callback(self._cur_time, skipped)
                    # check if password is already len()==4
                    self._check_password()
            self._buffer.append(aoi_id)
            self._password_entry_callback(self._cur_time, aoi_id)
            self._check_password()
            return

    def _check_password(self):
        # checks if the entered pattern is correct
        if self._buffer == self._password:
            self._buffer = []
            self._accept_password_callback(self._cur_time)
            return
        if len(self._buffer) == len(self._password):
            self._buffer = []
            self._reject_password_callback(self._cur_time)


# dictionary which checks the
skippable_dict = {
    1: {
        3: 2,
        7: 4,
        9: 5
    },
    2: {
        8: 5
    },
    3: {
        1: 2,
        7: 5,
        9: 6
    },
    4: {
        6: 5
    },
    5: {},
    6: {
        4: 5
    },
    7: {
        1: 4,
        3: 5,
        9: 8
    },
    8: {
        2: 5
    },
    9: {
        1: 5,
        7: 8,
        3: 6
    }
}
