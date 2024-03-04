from kivy.uix.screenmanager import ScreenManager

from .screen import SceneScreen


class SceneScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._active_screen = None

    def add_screen(self, screen: SceneScreen):
        self.add_widget(screen)

    def connect(self, source_screen: SceneScreen, target_screen: SceneScreen):
        source_screen.add_next_screen(target_screen.name)

    def next_screen(self):
        next_screen = self.current_screen.next_screen
        self.current = next_screen
