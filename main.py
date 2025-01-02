from time import time

import pyxel as px

from srcs.constants import (
    BLACK,
    PURPLE,
)
from srcs.base import Layer, Updatable
from srcs.player import Player
from srcs.utils import extract_obj_from_tilemap
from srcs.vector import Vector2D


class App:
    def load_map(self):
        self.x = 0
        self.y = 0
        self.bank = 0
        self.u = 0
        self.v = 0
        self.w = 128
        self.h = 64
        self.removes = extract_obj_from_tilemap(
            self.x, self.y, self.bank, self.u, self.v, self.w, self.h
        )

    def __init__(self):
        px.init(128, 128)
        px.load("./assets/pyxelvania.pyxres")
        self.t = time()

        self.player = Player(Vector2D(60, 40))
        self.load_map()

        px.run(self.update, self.draw)

    def update(self):
        current_t = time()
        dt = current_t - self.t
        self.t = current_t

        for o in Updatable.updatables:
            o.update(dt, self.t)

    def remove_obj_tile(self):
        for r in self.removes:
            px.rect((r[0] + r[2]) * 8, (r[1] + r[3]) * 8, 8, 8, BLACK)

    def draw(self):
        # px.camera(0, -px.frame_count // 8)
        px.cls(BLACK)
        px.bltm(self.x, self.y, self.bank, self.u, self.v, self.w, self.h, PURPLE)
        self.remove_obj_tile()

        for o in Layer.bg:
            o.draw()
        for o in Layer.obj:
            o.draw()
        for o in Layer.fg:
            o.draw()


App()
