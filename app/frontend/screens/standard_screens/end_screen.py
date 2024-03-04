from kivy.uix.button import Button
from kivy.uix.label import Label

from app.frontend.screens.screen import SceneScreen

TEXT = 'Thank you for your participation.'


class EndScreen(SceneScreen):
    """ Simple end-screen which just displays 'End' at the end of the study """

    def __init__(self, **kw):
        super().__init__(**kw)
        self._btn = Button(text='End')
        self._label = Label(text=TEXT, font_size='70sp')
        self.add_widget(self._label)
