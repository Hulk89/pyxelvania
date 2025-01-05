from typing import Union, TYPE_CHECKING

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
    ITEM_MAGICSTICK,
    ITEM_ENDGAME,
    ENEMY_1,
    ENEMY_2,
    ENEMY_3,
    ENEMY_4,
)
from srcs.objects import (
    EndGameObject,
    KeyObject,
    MagicStickObject,
    SlideObject,
    DJumpObject,
    CKPTObject,
    HeartObject,
    NPCObject1,
    NPCObject2,
)
from srcs.utils import get_tile
from srcs.vector import Vector2D
from srcs.enemies import Enemy1, Enemy2, Enemy3, Enemy4


class GameState:
    player: Union[None, "Player"] = None
    ## player state
    player_state = {
        "keys": 0,
        "hp": 2,
        "max_jump": 1,
        "damage": 2,
        "slide": False,
        "ckpt_pos": (0, 0),
        "max_bullet": 2,
    }
    map_state = []
    visited_map = set()
    eaten_item_pos = []


# TODO: this function should be here??
def extract_obj_from_tilemap(b, u, v, w, h):
    remove_obj = [
        NPC_1,
        NPC_2,
        ITEM_DBJMP,
        ITEM_SLIDE,
        ITEM_HEART,
        ITEM_CKPT,
        ITEM_KEY,
        ITEM_MAGICSTICK,
        ITEM_ENDGAME,
        ENEMY_1,
        ENEMY_2,
        ENEMY_3,
        ENEMY_4,
    ]

    removes = []
    for cx in range(u // 8, u // 8 + w // 8):
        for cy in range(v // 8, v // 8 + h // 8):
            tile = get_tile(cx, cy, b)
            if tile in remove_obj:
                removes.append((0, 0, cx, cy))
                pos = Vector2D(cx * 8, cy * 8)
                if pos in GameState.eaten_item_pos:
                    continue
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
                elif tile == ITEM_MAGICSTICK:
                    _ = MagicStickObject(pos)
                elif tile == ITEM_ENDGAME:
                    _ = EndGameObject(pos)
                elif tile == ENEMY_1:
                    _ = Enemy1(pos)
                elif tile == ENEMY_2:
                    _ = Enemy2(pos)
                elif tile == ENEMY_3:
                    _ = Enemy3(pos)
                elif tile == ENEMY_4:
                    _ = Enemy4(pos)
                elif tile == NPC_1:
                    _ = NPCObject1(pos)
                elif tile == NPC_2:
                    _ = NPCObject2(pos)

    return removes
