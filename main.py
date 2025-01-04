from time import time

import pyxel as px

from srcs.constants import BLACK, PURPLE, GREEN, RED, LOCKED_TILE, BLANK_TILE
from srcs.base import Layer, Updatable
from srcs.utils import colliding_wall
from srcs.objects import _Object, _AObject, CKPTObject
from srcs.player import Player
from srcs.fireball import FireBall
from srcs.particles import ParticlesExplosion
from srcs.enemies import Enemy
from srcs.state import GameState, extract_obj_from_tilemap
from srcs.map_util import parse_map, is_in
from srcs.vector import Vector2D


def locked_tile_update():
    player = GameState.player
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
            if not isinstance(o, CKPTObject):
                GameState.eaten_item_pos.append(o.pos)
            o.remove()


def attack_update():
    player = GameState.player
    enemies = [o for o in Layer.obj if isinstance(o, Enemy)]
    fireballs = [o for o in Layer.fg if isinstance(o, FireBall)]
    remove_objects = set()

    for e in enemies:
        e.direction_left = True if player.pos.x < e.pos.x else False
        if e.collide_with(player):
            ParticlesExplosion(
                player.pos + Vector2D(4, 4),
                [RED, RED, GREEN],
                duration=0.2,
                num_particles=10,
                vel_range=(5, 10),
            )
        for f in fireballs:
            if e.collide_with(f):
                e.hp -= GameState.player_state["damage"]
                if e.hp <= 0:
                    remove_objects.add(e)
                remove_objects.add(f)
    for r in remove_objects:
        r.remove()


class App:
    def load_map(self, idx):
        # NOTE: first, remove all enemies and objects
        for obj in reversed(Layer.obj):
            if isinstance(obj, Enemy):
                obj.remove()
            elif isinstance(obj, _Object) or isinstance(obj, _AObject):
                obj.remove()

        maps = GameState.map_state
        self.uvwh = tuple(p * 8 for p in maps[idx]["xywh"])
        self.doors = [(door[0] * 8, door[1] * 8, 8, 8) for door in maps[idx]["doors"]]
        self.link_to = maps[idx]["link_to"]
        self.removes = extract_obj_from_tilemap(0, *self.uvwh)

    def __init__(self):
        px.init(128, 128)
        px.load("./assets/pyxelvania.pyxres")
        GameState.map_state = parse_map(Vector2D(15, 6))
        self.t = time()

        GameState.player = Player(Vector2D(24, 10))
        GameState.player_state["ckpt_pos"] = (24, 10)
        self.load_map(0)

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

        p_pos = GameState.player.pos
        if not is_in(*p_pos, *self.uvwh):
            map_idx = -1
            min_dist = 10000
            for idx, door in zip(self.link_to, self.doors):
                door_center = Vector2D(door[0], door[1]) + Vector2D(4, 4)
                player_center = p_pos + Vector2D(4, 4)
                dist = (player_center - door_center).norm()
                if dist < min_dist:
                    map_idx = idx
                    min_dist = dist
            self.load_map(map_idx)

    def remove_obj_tile(self):
        for r in self.removes:
            px.rect((r[0] + r[2]) * 8, (r[1] + r[3]) * 8, 8, 8, BLACK)

    def draw(self):
        p_pos = GameState.player.pos
        cam_pos = p_pos - Vector2D(64, 32)
        px.camera(*cam_pos)
        px.cls(BLACK)
        px.bltm(self.uvwh[0], self.uvwh[1], 0, *self.uvwh, PURPLE)
        px.clip(0, 0, 128, 64)
        self.remove_obj_tile()

        for o in Layer.bg:
            o.draw()
        for o in Layer.obj:
            o.draw()
        for o in Layer.fg:
            o.draw()


App()
