from app.authenticator.touch_validator import TouchValidator
from app.config import config
from app.utils import EventManager, StorageHandler, Event
from app.utils.recording_helper import RecordingHelper

PASSWORD_LIST = config['PASSWORD_LIST']


class TouchAuthenticator:
    def __init__(self, recording_helper: RecordingHelper, end_authentication_callback):
        self._recording_helper = recording_helper
        self._end_authentication_callback = end_authentication_callback
        self.password = None
        self._board = None
        self._draw = config['draw']
        self._event_manager = EventManager()
        self._validator: TouchValidator = None
        self._storage_handler = StorageHandler(modality='Touch')
        self._auth_started = False
        self._attempt = 1
        self._scenario = 0

    def start(self):
        # get password
        self.password = PASSWORD_LIST[self._scenario]
        # init validator
        self._validator = TouchValidator(
            self.on_password_entry,
            self._accept_password,
            self._reject_password,
            self.password
        )

    def stop(self):
        self._end()

    def get_scenario(self):
        return self._scenario

    def _end(self):
        self._event_manager.add_event(Event.from_end_event())
        self._recording_helper.stop()
        # save data
        self._storage_handler.save(events=self._event_manager.get_events(),
                                   scenario=str(self._scenario), scenario_attempt=self._attempt)
        self._event_manager.clear()
        self._end_authentication_callback()

    def password_entry_confirmed(self):
        self._scenario += 1
        self._attempt = 1

    @property
    def scenario(self):
        return self._scenario

    @property
    def attempt(self):
        return self._attempt

    def password_entry_rejected(self):
        self._attempt += 1

    def _accept_password(self, timestamp):
        self._event_manager.add_event(Event.from_password_recognized(timestamp))
        self._end()

    def _reject_password(self, timestamp):
        self._event_manager.add_event(Event.from_failed_authentication(timestamp))
        self._end()

    def add_event(self, event: Event):
        self._event_manager.add_event(event)

    def start_validating(self):
        self._validator.validate()
        pass

    def on_password_entry(self, timestamp, password):
        self._event_manager.add_event(Event.from_password(timestamp, password))
        pass

    def on_aoi_activation(self, timestamp, aoi_id):
        self._validator.add_activation(timestamp, aoi_id)
