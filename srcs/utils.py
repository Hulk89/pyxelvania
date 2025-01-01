import pyxel as px

TILE_FLOOR  = (1, 3)
WALL_TILE   = (0, 2)
SLIDE_FLOOR = (1, 2)


def get_tile(tile_x, tile_y, bank=0):
    return px.tilemaps[bank].pget(tile_x, tile_y)


def is_colliding(x, y, is_falling, is_sliding=False):
    x1 = px.floor(x) // 8
    y1 = px.floor(y) // 8
    x2 = (px.ceil(x) + 7) // 8
    y2 = (px.ceil(y) + 7) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi) == WALL_TILE:
                return True
            if get_tile(xi, yi) == SLIDE_FLOOR and not is_sliding:
                return True
    if is_falling and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) == TILE_FLOOR:
                return True
    return False


def push_back(x, y, dx, dy, is_sliding=False):
    for _ in range(px.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_colliding(x, y + step, dy > 0, is_sliding):
            break
        y += step
        dy -= step
    for _ in range(px.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_colliding(x + step, y, dy > 0, is_sliding):
            break
        x += step
        dx -= step
    return x, y


def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == TILE_FLOOR or tile == WALL_TILE

