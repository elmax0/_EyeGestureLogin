from kivy.core.window import Window
from kivy.uix.label import Label

from app.frontend.screens.screen import SceneScreen

TEXT = 'Start'


class GazeStartScreen(SceneScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._active = False
        Window.bind(on_key_down=self.on_key_down)
        self._label = Label(text=TEXT, font_size='70sp')
        # self.add_widget(self._btn)
        self.add_widget(self._label)

    def on_key_down(self, *args):
        if self._active:
            if args[1] == 32:
                self.switch_screen()

    def on_enter(self, *args):
        self._active = True

    def on_leave(self, *args):
        self._active = False
