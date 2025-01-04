from typing import Union, TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from srcs.player import Player
from srcs.constants import (
    NPC_1,
    NPC_2,
    ITEM_KEY,
    ITEM_CKPT,
    ITEM_HEART,
    ITEM_SLIDE,
    ITEM_DBJMP,
    ENEMY_1,
    ENEMY_2,
    ENEMY_3,
    ENEMY_4,
    DOOR_TILE_R,
    DOOR_TILE_L,
    WALL_TILE,
)
from srcs.objects import KeyObject, SlideObject, DJumpObject, CKPTObject, HeartObject
from srcs.utils import get_tile
from srcs.vector import Vector2D
from srcs.enemies import Enemy1, Enemy2, Enemy3, Enemy4


class GameState:
    player : Union[None, 'Player'] = None
    ## player state
    player_state = {
        "keys": 0,
        "hp": 2,
        "max_jump": 1,
        "damage": 2,
        "slide": False,
        "ckpt_pos": (0, 0)
    }
    map_state = {"maps": []}

def _is_rectangle(x, y, w, h):
    for x_i in range(x, x + w):
        if get_tile(x_i, y) not in [DOOR_TILE_L, DOOR_TILE_R, WALL_TILE]:
            return False
        if get_tile(x_i, y + h - 1) not in [DOOR_TILE_L, DOOR_TILE_R, WALL_TILE]:
            return False
    for y_i in range(y, y + h):
        if get_tile(x, y_i) not in [DOOR_TILE_L, DOOR_TILE_R, WALL_TILE]:
            return False
        if get_tile(x + w - 1, y_i)not in [DOOR_TILE_L, DOOR_TILE_R, WALL_TILE]:
            return False
    return True

def _find_doors(x, y, w, h):
    doors = []
    for x_i in range(x, x + w):
        if get_tile(x_i, y) in [DOOR_TILE_L, DOOR_TILE_R]:
            doors.append((x_i, y))
        if get_tile(x_i, y + h - 1) in [DOOR_TILE_L, DOOR_TILE_R]:
            doors.append((x_i, y + h - 1))
    for y_i in range(y, y + h):
        if get_tile(x, y_i) in [DOOR_TILE_L, DOOR_TILE_R]:
            doors.append((x, y_i))
        if get_tile(x + w - 1, y_i) in [DOOR_TILE_L, DOOR_TILE_R]:
            doors.append((x + w - 1, y_i))
    return doors


def _is_in(xx, yy, x, y, w, h):
    return xx >= x and xx < x+w and yy >= y and yy < y+h

def _link_doors_to_map(maps):
    for i, curr_map in enumerate(maps):
        link_to = []
        for door in curr_map["doors"]:
            find_pos = Vector2D(door[0], door[1])
            if get_tile(door[0], door[1]) == DOOR_TILE_R:
                find_pos += Vector2D(1, 0)
            else:
                find_pos += Vector2D(-1, 0)

            for j, cand_map in enumerate(maps):
                if i == j:
                    continue
                if _is_in(*find_pos, *cand_map["xywh"]):
                    link_to.append(j)
        curr_map["link_to"] = link_to



def load_map(start_door=Vector2D(0, 0), max_search=64):
    maps = []

    def find_contour(s_x, s_y) -> Tuple[int, int, int, int]:
        # NOTE: 공간은 항상 직사각형이며, WALL_TILE과 DOOR_TILE_<R,L> 로 이루어져있다고 가정한다.
        left = -1
        right = -1
        top = -1
        bottom = -1

        if get_tile(s_x, s_y) == DOOR_TILE_R:  # NOTE: 오른쪽 벽
            right = s_x
        else:
            left = s_x
            

        # NOTE: floor only can wall_tile >= 16
        for y_i in range(1, max_search):
            if left != -1:
                if _is_rectangle(s_x, s_y + y_i, 16, 1):
                    bottom = s_y + y_i
            else:
                if _is_rectangle(s_x - 15, s_y + y_i, 16, 1):
                    bottom = s_y + y_i
            if bottom != -1:
                break

        for y_i in range(1, max_search):
            if left != -1:
                if _is_rectangle(s_x, s_y - y_i, 16, 1):
                    top = s_y - y_i
            else:
                if _is_rectangle(s_x - 15, s_y - y_i, 16, 1):
                    top = s_y - y_i
            if top != -1:
                break

        for x_i in range(1, max_search):
            if left != -1:
                if _is_rectangle(left, top, 1, bottom -  top + 1):
                    right = left + x_i
                    break
            else:
                if _is_rectangle(right-x_i, top, 1, bottom - top + 1):
                    left = right - x_i
                    break
        return (left, right, top, bottom)

    def _load_map(start_pos):
        lrtb = find_contour(*start_pos)
        left, right, top, bottom = lrtb
        xywh = (left, top, right - left + 1, bottom - top + 1)
        doors = _find_doors(*xywh)
        maps.append({"xywh": xywh, "doors": doors})
        for d_x, d_y in doors:
            
            s_pos = Vector2D(d_x, d_y)
            if get_tile(d_x, d_y) == DOOR_TILE_R:
                s_pos += Vector2D(1, 0)
            else:
                s_pos += Vector2D(-1, 0)

            for map in maps:
                if _is_in(*s_pos, *map["xywh"]):
                    break
            else:
                _load_map(s_pos)

    _load_map(start_door)
    _link_doors_to_map(maps)

    return maps

def extract_obj_from_tilemap(b, u, v, w, h):
    remove_obj = [
        NPC_1,
        NPC_2,
        ITEM_DBJMP,
        ITEM_SLIDE,
        ITEM_HEART,
        ITEM_CKPT,
        ITEM_KEY,
        ENEMY_1,
        ENEMY_2,
        ENEMY_3,
        ENEMY_4,
    ]

    removes = []
    for cx in range(u, u + w // 8):
        for cy in range(v, v + h // 8):
            tile = get_tile(cx, cy, b)
            # TODO: make_object
            if tile in remove_obj:
                removes.append((0, 0, cx, cy))
                pos = Vector2D(cx * 8, cy * 8)
                if tile == ITEM_KEY:
                    _ = KeyObject(pos)
                elif tile == ITEM_HEART:
                    _ = HeartObject(pos)
                elif tile == ITEM_SLIDE:
                    _ = SlideObject(pos)
                elif tile == ITEM_DBJMP:
                    _ = DJumpObject(pos)
                elif tile == ITEM_CKPT:
                    _ = CKPTObject(pos)
                elif tile == ENEMY_1:
                    _ = Enemy1(pos)
                elif tile == ENEMY_2:
                    _ = Enemy2(pos)
                elif tile == ENEMY_3:
                    _ = Enemy3(pos)
                elif tile == ENEMY_4:
                    _ = Enemy4(pos)

    return removes
