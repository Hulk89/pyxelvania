from time import time

import pyxel as px
from rich import print

from srcs.constants import BLACK
from srcs.base import Layer, Updatable
from srcs.player import Player
class App:
    def __init__(self):
        px.init(160, 120)
        px.load("./assets/pyxelvania.pyxres")
        self.t = time()        

        self.player = Player((60, 60))
        self.player.set_draw_layer(Layer.obj)
        px.run(self.update, self.draw)


    def update(self):
        current_t = time()
        dt = self.t - current_t
        self.t = current_t
        
        print("B", self.player.pos)
        for o in Updatable.updatables:
            o.update(dt, self.t)
        print("A", self.player.pos)
        
    def draw(self):
        px.cls(BLACK)
        for o in Layer.bg:
            o.draw()
        for o in Layer.obj:
            o.draw()
        for o in Layer.fg:
            o.draw()


App()
