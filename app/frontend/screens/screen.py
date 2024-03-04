from kivy.uix.screenmanager import Screen


class SceneScreen(Screen):
    """
    Own Screen class that can be connected with other screens
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self._next_screen = None

    def add_next_screen(self, next_screen):
        if self._next_screen:
            raise Exception(f"{self.name} already has next_screen and cant add {next_screen}")
        self._next_screen = next_screen

    def switch_screen(self, event=None):
        self.parent.next_screen()

    @property
    def next_screen(self):
        return self._next_screen
