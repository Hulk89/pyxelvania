from time import time

import pyxel as px

from srcs.constants import (
    BLACK,
    PURPLE,
    GREEN,
    RED,
    LOCKED_TILE,
    BLANK_TILE
)
from srcs.base import Layer, Updatable
from srcs.player import Player
from srcs.fireball import FireBall
from srcs.particles import ParticlesExplosion
from srcs.enemies import Enemy
from srcs.utils import colliding_wall
from srcs.objects import _Object, _AObject

from srcs.state import GameState, extract_obj_from_tilemap
from srcs.vector import Vector2D


def locked_tile_update():
    player = GameState.player
    # NOTE: remove locked tile
    # TODO: only when keys are added. maybe it will added to gamestate
    if player.direction_right:
        check_pos = player.pos + Vector2D(1, 0)
    else:
        check_pos = player.pos + Vector2D(-1, 0)
    tile, tile_pos = colliding_wall(*check_pos, player.dy > 0)
    if tile == LOCKED_TILE and GameState.player_state["keys"] > 0:
        GameState.player_state["keys"] -= 1
        px.tilemaps[0].pset(*tile_pos, BLANK_TILE)


def object_update():
    player = GameState.player

    objs = [o for o in Layer.obj if isinstance(o, _Object) or isinstance(o, _AObject)]

    for o in objs:
        if o.collide_with(player):
            o.update_gamestate(GameState.player_state)
            o.remove()

def attack_update():
    player = GameState.player
    fireballs = [o for o in Layer.fg if isinstance(o, FireBall)]
    enemies = [o for o in Layer.obj if isinstance(o, Enemy)]

    for e in enemies:
        e.direction_left = True if player.pos.x < e.pos.x else False
        if e.collide_with(player):
            ParticlesExplosion(player.pos + Vector2D(4, 4),
                               [RED, RED, GREEN],
                               duration=0.2,
                               num_particles=10,
                               vel_range=(5, 10))
        for f in fireballs:
            if e.collide_with(f):
                f.remove()
                e.hp -= GameState.player_state["damage"]
                if e.hp <= 0:
                    e.remove()
    

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

        GameState.player = Player(Vector2D(24, 10))
        GameState.player_state["ckpt_pos"] = (24, 10)
        self.load_map()

        px.run(self.update, self.draw)

    def update(self):
        current_t = time()
        dt = current_t - self.t
        self.t = current_t

        object_update()
        attack_update()
        locked_tile_update()

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
