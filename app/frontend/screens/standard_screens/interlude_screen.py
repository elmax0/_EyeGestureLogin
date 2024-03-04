from kivy.core.window import Window
from kivy.uix.label import Label

from app.frontend.screens.screen import SceneScreen

DURATION = 2

TEXT = 'Now please look at the appearing points \n until they disappear'


class InterludeScreen(SceneScreen):
    """ Just a simple screen which introduces the accuracy/precision process before starting it"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self._active = False
        self._label = Label(text=TEXT, font_size='50sp')
        self.add_widget(self._label)
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, *args):
        if self._active:
            if args[1] == 32:
                self.switch_screen()

    def on_enter(self, *args):
        self._active = True

    def on_leave(self, *args):
        self._active = False
        self.clear_widgets()
        pass
