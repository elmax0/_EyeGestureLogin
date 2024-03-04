import logging
import os
from os import path

from depthai_recorder import Recorder

from app.config import config

PARTICIPANT = config['participant']
VIDEO_ROOT = config['video_root']
TRAINING = config['training']

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)


class RecordingHelper:
    def __init__(self, modality='Gaze'):
        if TRAINING:
            return
        # self._video_root = path.join(VIDEO_ROOT, PARTICIPANT)
        self._modality = modality
        if not path.exists(VIDEO_ROOT):
            os.mkdir(VIDEO_ROOT)
        self._participant_root = path.join(VIDEO_ROOT, PARTICIPANT)
        if not path.exists(self._participant_root):
            os.mkdir(self._participant_root)
        self._modality_folder = path.join(self._participant_root, self._modality)
        if not path.exists(self._modality_folder):
            os.mkdir(self._modality_folder)
        self._recorder = Recorder(convert_to_mp4=True, output_path=self._modality_folder, ffmpeg_log=False,
                                  camera_iso=200, camera_exposure=17000, camera_focus=132)

    def start(self, scenario, attempt):
        if TRAINING:
            return
        rec_id = f"{scenario}_{attempt}"
        if TRAINING:
            rec_id = f"{rec_id}_TRAINING"
        rec_path = path.join(self._modality_folder, rec_id)
        if not path.exists(rec_path):
            os.mkdir(rec_path)
        self._recorder.start_video_recording(rec_id=rec_id)
        pass

    def stop(self):
        if TRAINING:
            return
        self._recorder.stop_video_recording()
        pass

    def end(self):
        print("END")
        self._recorder.process.terminate()
        self._recorder.process.join()
        pass
