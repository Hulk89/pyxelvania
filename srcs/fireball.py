import pyxel as px

from .constants import PURPLE, ORANGE, YELLOW
from .base import (
    Updatable,
    Drawable,
    CircleCollisionInterface,
    Sprite,
    Image,
    Layer
)
from .particles import ParticlesExplosion
from .utils import colliding_wall

FIREBALL = (32, 8, 3, 3)
DX = 60


class FireBall(CircleCollisionInterface, Updatable, Drawable):
    def __init__(self, pos, direction_right):
        self.dx = DX if direction_right else -DX
        self.sprite = Sprite(Image(*FIREBALL), PURPLE)
        super().__init__(pos, 3, 3)
        self.set_draw_layer(Layer.fg)
        self.start_update()

    def update(self, dt, t):
        x, y = self.pos
        x += int(self.dx * dt)
        self.pos = (x, y)

        tile, _ = colliding_wall(x, y, False, False, 3)
        if tile:
            self.remove()

    def draw(self):
        self.sprite.draw(self.pos)

    def remove(self):
        ParticlesExplosion(
            self.pos,
            [ORANGE, YELLOW, PURPLE],
            vel_range=(10, 20),
            num_particles=30,
            acceleration=-1,
        )
        self.stop_draw()
        self.stop_update()
