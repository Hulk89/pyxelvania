import pyxel as px

from .constants import WHITE, RED
from .base import (
    CircleCollisionInterface,
    Updatable,
    Drawable,
    ASprite,
    Image,
    Layer,
)

from .vector import Vector2D
from .utils import push_back

ENEMY_1_DICT = {
    "run": {"frames": [(40, 0, 8, 8), (48, 0, 8, 8)], "loop": True},
}

ENEMY_2_DICT = {
    "run": {"frames": [(40, 8, 8, 8), (48, 8, 8, 8)], "loop": True},
}


ENEMY_3_DICT = {
    "run": {"frames": [(56, 0, 8, 8), (64, 0, 8, 8)], "loop": True},
}


ENEMY_4_DICT = {
    "run": {"frames": [(56, 8, 8, 8), (64, 8, 8, 8)], "loop": True},
}


class Enemy(CircleCollisionInterface, Updatable, Drawable):
    def __init__(self, pos, info_dict, freq, hp, vel=2, atk=1):
        self.max_hp = self.hp = hp
        self.direction_left = True
        self.dx = 0
        self.dy = 0
        self.atk = atk
        self.vel = vel
        self.state = "run"
        self.asprites = {
            k: ASprite([Image(*uvwh) for uvwh in v["frames"]], freq, loop=v["loop"])
            for k, v in info_dict.items()
        }
        super().__init__(pos, 8, 8)
        self.start_update()
        self.set_draw_layer(Layer.obj)

    @property
    def sprite(self):
        return self.asprites[self.state]

    @property
    def img(self):
        return self.sprite.img

    def update(self, dt, t):
        self.dy += 0.5 * dt

        # NOTE: position update
        if self.direction_left:
            self.dx = -self.vel * dt
        else:
            self.dx = self.vel * dt
        self.dy = min(4, max(-6, self.dy))
        x, y = push_back(*self.pos, self.dx, self.dy)  # NOTE: circular import
        self.pos = Vector2D(x, int(y))

        # NOTE: sprite update frame
        self.sprite.update(dt, t)

    def draw(self):
        self.img.flip = self.direction_left == False
        self.sprite.draw(self.pos)
        if self.hp != self.max_hp:
            px.rect(*(self.pos + Vector2D(0, 8)), 8, 3, WHITE)
            px.rect(*(self.pos + Vector2D(1, 9)), (self.hp * 6) // self.max_hp, 1, RED)

    def remove(self):
        self.stop_draw()
        self.stop_update()
        del self


class Enemy1(Enemy):
    def __init__(self, pos):
        super().__init__(pos, ENEMY_1_DICT, 0.4, 1, 1)


class Enemy2(Enemy):
    def __init__(self, pos):
        super().__init__(pos, ENEMY_2_DICT, 0.2, 8, 2)


class Enemy3(Enemy):
    def __init__(self, pos):
        super().__init__(pos, ENEMY_3_DICT, 0.4, 5, 3, 2)


class Enemy4(Enemy):
    def __init__(self, pos):
        super().__init__(pos, ENEMY_4_DICT, 0.2, 20, 8, 2)
