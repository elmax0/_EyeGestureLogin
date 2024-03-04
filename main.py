from app.frontend.frontend import Frontend
from app.utils.recording_helper import RecordingHelper
from app.config import config


TRAINING = config['training']
MODALITY = config['modality']
SET_SIZE = config['set_size']
DRAWING = False

if __name__ == '__main__':
    recording_helper = RecordingHelper(MODALITY)
    Frontend(recording_helper=recording_helper, modality=MODALITY, training=TRAINING, drawing=DRAWING,
             set_size=SET_SIZE).run()