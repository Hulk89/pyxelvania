from time import time

import pyxel as px

from srcs.constants import BLACK, PURPLE, LOCKED_TILE, BLANK_TILE, WIDTH, HEIGHT
from srcs.base import Layer, Updatable
from srcs.utils import colliding_wall
from srcs.objects import _Object, _AObject, CKPTObject, NPCObject1, NPCObject2
from srcs.player import Player
from srcs.fireball import FireBall
from srcs.enemies import Enemy
from srcs.state import GameState, extract_obj_from_tilemap
from srcs.map_util import parse_map, is_in
from srcs.vector import Vector2D
from srcs.hud import MiniMapHUD, PlayerItemsHUD


def locked_tile_update():
    player = GameState.player
    if player is None:
        return

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
            if not (
                isinstance(o, CKPTObject)
                or isinstance(o, NPCObject1)
                or isinstance(o, NPCObject2)
            ):
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
            player.damaged(e.direction_left, e.atk)

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
        GameState.visited_map.add(idx)

    def __init__(self):
        px.init(128, 128)
        px.load("./assets/pyxelvania.pyxres")
        self.t = time()
        # (24, 10), (15, 6)
        # (24, 688), (15, 86)
        start_pos = (24, 688)
        start_door_pos = Vector2D(15, 86)
        GameState.map_state = parse_map(start_door_pos)
        GameState.player = Player(Vector2D(0, 0), GameState.player_state["hp"])
        GameState.player_state["ckpt_pos"] = start_pos
        PlayerItemsHUD()
        MiniMapHUD()
        self.reset()
        px.run(self.update, self.draw)

    def reset(self):
        GameState.player.pos = Vector2D(*GameState.player_state["ckpt_pos"])
        for i, map in enumerate(GameState.map_state):
            uvwh = tuple(p * 8 for p in map["xywh"])
            if is_in(*GameState.player.pos, *uvwh):
                self.load_map(i)
                GameState.player.hp = GameState.player_state["hp"]
                GameState.player.is_damaged = True
                GameState.player.damaged_time = time()
                break

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
        if GameState.player.hp <= 0:
            self.reset()

    def remove_obj_tile(self):
        for r in self.removes:
            px.rect((r[0] + r[2]) * 8, (r[1] + r[3]) * 8, 8, 8, BLACK)

    def draw(self):
        p_pos = GameState.player.pos
        cam_pos = p_pos - Vector2D(WIDTH // 2, HEIGHT // 4)
        px.camera(*cam_pos)
        px.cls(BLACK)

        px.clip(0, 0, WIDTH, HEIGHT // 2)
        px.bltm(self.uvwh[0], self.uvwh[1], 0, *self.uvwh, PURPLE)
        self.remove_obj_tile()

        for o in Layer.bg:
            o.draw()
        for o in Layer.obj:
            o.draw()
        for o in Layer.fg:
            o.draw()
        px.clip()
        for o in Layer.hud:
            o.draw()
        for o in Layer.popup_text:
            o.draw()


App()
