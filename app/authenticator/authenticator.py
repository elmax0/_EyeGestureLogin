from app.authenticator.gaze import Fixation, GazeHandler
from app.authenticator.validator import Validator
from app.config import config
from app.utils import Event, EventManager, StorageHandler
from app.utils.recording_helper import RecordingHelper

PASSWORD_LIST = config['PASSWORD_LIST']
TRAINING = config['training']


class Authenticator:
    """
    The Authenticator class manages the gaze-based authentication process.

    Args:
        recording_helper (RecordingHelper): An instance of RecordingHelper to manage recording.
        end_authentication_callback: Callback function to signal the end of authentication.
        fixation_callback: Callback function to handle fixation events.
        offset_callback: Callback function to handle offset events.
        start_animation_callback: Callback function to start animations.
        stop_animation_callback: Callback function to stop animations.
    """

    def __init__(self, recording_helper: RecordingHelper,
                 end_authentication_callback, fixation_callback,
                 offset_callback, start_animation_callback, stop_animation_callback):
        self._end_authentication_callback = end_authentication_callback
        self._offset_callback = offset_callback
        self._fixation_callback = fixation_callback
        self._start_animation_callback = start_animation_callback
        self._stop_animation_callback = stop_animation_callback
        self.password = None
        self._validator = None
        self._recording_helper = recording_helper
        self._gaze_handler = GazeHandler(self._on_fixation,
                                         self._start_animation,
                                         self._stop_animation,
                                         self._start_authentication_process,
                                         self._on_offset,
                                         self._on_start_offset_calculation,
                                         self._on_offset_calculation_failed,
                                         self._on_eyes_recognized)
        self._draw = config['draw']
        self._event_manager = EventManager()
        self._storage_handler = StorageHandler()
        self._auth_started = False
        self._attempt = 1
        self._scenario = 0

    def start(self):
        # on start, get the current pattern and initialize the validator with said pattern and start the gaze handler
        self.password = PASSWORD_LIST[self._scenario]
        self._validator = Validator(self._on_password_entry, self._accept_password, self._reject_password,
                                    password=self.password)
        self._event_manager.add_event(Event.from_start_event())
        self._gaze_handler.start()

        # add start_recording events to the event-handler
        self._event_manager.add_event(Event.from_start_recording())
        # start recording
        self._recording_helper.start(self._scenario, self._attempt)

    def stop(self):
        self._gaze_handler.stop()
        self._auth_started = False

    def stop_all_authentication(self):
        self._gaze_handler.stop_all_authentication()

    def password_entry_confirmed(self):
        self._scenario += 1
        self._attempt = 1

    def password_entry_rejected(self):
        self._attempt += 1

    def get_scenario(self):
        return self._scenario

    def _end(self):
        # add event from stop recording
        self._event_manager.add_event(Event.from_stop_recording())
        # stop recording
        self._recording_helper.stop()
        raw_data = self._gaze_handler.get_raw_data()
        self._gaze_handler.stop()
        self._auth_started = False

        self._event_manager.add_event(Event.from_end_event())
        # save events and raw_data
        self._storage_handler.save(events=self._event_manager.get_events(), raw_data=raw_data,
                                   scenario=str(self._scenario), scenario_attempt=self._attempt)
        self._event_manager.clear()
        self._end_authentication_callback()

    def _on_fixation(self, aoi_id, fixation: Fixation):
        # add fixation-event
        self._event_manager.add_event(Event.from_fixation(fixation))
        # transfer aoi_id and fixation to the validator
        self._validator.add_fixation(aoi_id, fixation)
        # draw the fixation (if wanted)
        if self._draw:
            self._fixation_callback(fixation)

    def _on_password_entry(self, timestamp, password):
        self._event_manager.add_event(Event.from_password(timestamp, password))

    def _accept_password(self, timestamp):
        self._event_manager.add_event(Event.from_password_recognized(timestamp))
        self._end()

    def _reject_password(self, timestamp):
        self._event_manager.add_event(Event.from_failed_authentication(timestamp))
        self._end()

    def _on_offset(self, timestamp, offset):
        self._event_manager.add_event(Event.from_offset(timestamp, offset))
        self._offset_callback()

    def _on_start_offset_calculation(self, timestamp):
        self._event_manager.add_event(Event.from_start_offset_calculation(timestamp))

    def _on_offset_calculation_failed(self, timestamp):
        self._event_manager.add_event(Event.from_offset_calculation_failed(timestamp))

    def _on_eyes_recognized(self, timestamp):
        self._event_manager.add_event(Event.from_eyes_detected(timestamp))

    def _start_animation(self, timestamp):
        self._event_manager.add_event(Event.from_start_animation(timestamp))
        self._start_animation_callback()

    def _stop_animation(self, timestamp):
        self._event_manager.add_event(Event.from_stop_animation(timestamp))
        self._stop_animation_callback()

    def _start_authentication_process(self):
        self._auth_started = True
        self._gaze_handler.start_authentication()
        self._event_manager.add_event(Event.from_start_authentication())
