class TouchValidator:

    def __init__(self, password_entry_callback, accept_password_callback, reject_password_callback, password):
        self._password_entry_callback = password_entry_callback
        self._accept_password_callback = accept_password_callback
        self._reject_password_callback = reject_password_callback
        self._password = password
        self._buffer = []
        self._cur_time = None

    def add_activation(self, timestamp, aoi_id):
        # add aoi_id unless it is the same aoi_id as the last entry
        self._cur_time = timestamp
        if len(self._buffer) == 0:
            self._buffer.append(aoi_id)
            self._password_entry_callback(self._cur_time, aoi_id)
            return
        if self._buffer[-1] != aoi_id:
            # add aoi_id as new password entry
            self._buffer.append(aoi_id)
            self._password_entry_callback(self._cur_time, aoi_id)
            return

    def validate(self):
        self._check_password()
        pass

    def _check_password(self):
        if self._buffer == self._password:
            self._buffer = []
            self._accept_password_callback(self._cur_time)
            return
        if len(self._buffer) >= len(self._password):
            self._buffer = []
            self._reject_password_callback(self._cur_time)
