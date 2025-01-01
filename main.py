from time import time

import pyxel as px

from srcs.constants import BLACK, PURPLE
from srcs.base import Layer, Updatable
from srcs.player import Player


class App:
    def __init__(self):
        px.init(128, 128)
        px.load("./assets/pyxelvania.pyxres")
        self.t = time()
        self.player = Player((60, 40))
        px.run(self.update, self.draw)

    def update(self):
        current_t = time()
        dt = current_t - self.t
        self.t = current_t

        for o in Updatable.updatables:
            o.update(dt, self.t)

    def draw(self):
        px.cls(BLACK)
        px.bltm(0, 0, 0, 0, 0, 128, 128, PURPLE)
        for o in Layer.bg:
            o.draw()
        for o in Layer.obj:
            o.draw()
        for o in Layer.fg:
            o.draw()


App()
