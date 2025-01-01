import pyxel as px
from .constants import (
    FLOOR_TILE,
    WALL_TILE,
    SLIDE_TILE,
    LOCKED_TILE,
    DOOR_TILE_R,
    DOOR_TILE_L,
)


def get_tile(tile_x, tile_y, bank=0):
    return px.tilemaps[bank].pget(tile_x, tile_y)


def colliding_wall(x, y, is_falling, is_sliding=False, size=8):
    x1 = px.floor(x) // 8
    y1 = px.floor(y) // 8
    x2 = (px.ceil(x) + size - 1) // 8
    y2 = (px.ceil(y) + size - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            tile = get_tile(xi, yi)
            if tile in [WALL_TILE, LOCKED_TILE, DOOR_TILE_L, DOOR_TILE_L] or (
                tile == SLIDE_TILE and not is_sliding
            ):
                return tile
    if is_falling and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) == FLOOR_TILE:
                return FLOOR_TILE
    return False


def push_back(x, y, dx, dy, is_sliding=False):
    for _ in range(px.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if colliding_wall(x, y + step, dy > 0, is_sliding):
            break
        y += step
        dy -= step
    for _ in range(px.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if colliding_wall(x + step, y, dy > 0, is_sliding):
            break
        x += step
        dx -= step
    return x, y


def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == FLOOR_TILE or tile == WALL_TILE
