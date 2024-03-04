from kivy.core.window import Window

from app.frontend.gaze_frontend import GazeFrontend
from app.frontend.touch_frontend import TouchFrontend


class Frontend:
    """
        The Frontend class manages the user interface based on the selected modality (Gaze or Touch).

        Args:
            recording_helper: Instance of the RecordingHelper for managing recording.
            modality (str): The modality for user interaction. Options: 'Gaze' or 'Touch'.
            training (bool): Flag indicating whether the interface is in training mode.
            drawing (bool): Flag indicating whether drawing is enabled.
            set_size (int): Size of the pattern set.
            participant (str): Participant's identifier.
    """

    def __init__(self, recording_helper, modality='Gaze', training=False, drawing=False, set_size=15,
                 participant="Test"):
        Window.fullscreen = 'auto'
        self.modality = modality
        self.training = training
        self.drawing = drawing
        self.set_size = set_size
        self._recording_helper = recording_helper
        # select gaze- or touch-frontend depending on modality
        if self.modality != 'Gaze':
            self.frontend = TouchFrontend(self._recording_helper, training=self.training, drawing=self.drawing,
                                          set_size=self.set_size)
        else:
            self.frontend = GazeFrontend(self._recording_helper, training=self.training, drawing=self.drawing,
                                         set_size=self.set_size)

    def run(self):
        self.frontend.run()
