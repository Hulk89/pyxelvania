import pyxel as px

from .constants import PURPLE
from .base import (
    Updatable,
    Drawable,
    CircleCollisionInterface,
    Sprite,
    Image,
)

from .utils import colliding_wall

FIREBALL = (32, 8, 3, 3)
DX = 60


class FireBall(CircleCollisionInterface, Updatable, Drawable):
    def __init__(self, pos, direction_right):
        self.dx = DX if direction_right else -DX
        print(self.dx)
        self.sprite = Sprite(Image(*FIREBALL), PURPLE)
        super().__init__(pos, 3, 3)

    def update(self, dt, t):
        x, y = self.pos
        x += int(self.dx * dt)
        self.pos = (x, y)

        if colliding_wall(x + 1, y, False, False, 3):
            self.stop_draw()
            self.stop_update()
            del self

    def draw(self):
        self.sprite.draw(self.pos)
