from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import PushMatrix, Rotate, PopMatrix, Scale
from kivy.properties import NumericProperty
from kivy.uix.image import Image

from app.config import config

ANIMATION_SCALE = .2
SCALE_DURATION = 2
ROTATION_DURATION = 5

AVATAR_SIZE = config['AVATAR_SIZE']


class AnimationImage(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle = 0
            self.rot.origin = self.center
            self.rot.axis = (0, 0, 1)

            self.scale = Scale()
            # self.scale = self.rot.scale()
            self.scale.xyz = (1, 1, 1)
            self.scale.origin = self.rot.origin
        with self.canvas.after:
            PopMatrix()

        self._scale_animation = Animation(scale=ANIMATION_SCALE, duration=SCALE_DURATION)
        self.size_hint = None, None
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.angle = 0
        self._should_animate = False

    def animation_complete(self, *args):
        self.rot.angle = 0
        Clock.schedule_once(lambda dt: self._rotation_animation.stop(self.rot), 0)

        if self._should_animate:
            self._rotate()

    def set_center(self, x, y):
        self.rot.origin = (x, y)
        self.scale.origin = (x, y)

    def stop_animation(self):
        self._should_animate = False
        self.rot.angle = 0
        self.scale.xyz = (1, 1, 1)
        Clock.schedule_once(lambda dt: self._rotation_animation.stop(self.rot), 0)
        Clock.schedule_once(lambda dt: self._rotation_animation.cancel(self.rot), 0)
        Clock.schedule_once(lambda dt: self._scale_animation.stop(self.scale), 0)
        Clock.schedule_once(lambda dt: self._scale_animation.cancel(self.scale), 0)

        self._scale_animation.cancel(self.scale)
        self.rot.angle = 0

        self.scale.xyz = (1, 1, 1)

    def _rotate(self):
        self._rotation_animation = Animation(angle=-3600, duration=ROTATION_DURATION)
        self._rotation_animation.bind(on_complete=self.animation_complete)
        self._rotation_animation.repeat = True
        Clock.schedule_once(lambda dt: self._rotation_animation.start(self.rot), 0)

    def _scale_down(self):
        self.scale.xyz = (1, 1, 1)
        self._scale_animation = Animation(scale=ANIMATION_SCALE, duration=SCALE_DURATION)
        self._scale_animation.start(self.scale)

    def start_animation(self):
        self._should_animate = True
        self._rotate()
        self._scale_down()
