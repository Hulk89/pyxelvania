import pyxel as px

from srcs.constants import RED, WHITE, WIDTH, HEIGHT, YELLOW, ORANGE
from srcs.state import GameState
from srcs.base import Image, Layer, Drawable, Sprite
from srcs.vector import Vector2D
from srcs.map_util import is_in


class PlayerItemsHUD(Drawable):
    def __init__(self):
        self.pos = Vector2D(-WIDTH // 2, HEIGHT // 4)

        self.sprites = {
            "key": Sprite(Image(16, 16, 8, 8)),
            "damaged-hp": Sprite(Image(32, 40, 8, 8)),
            "hp": Sprite(Image(16, 40, 8, 8)),
            "slide": Sprite(Image(0, 40, 8, 8)),
            "jump": Sprite(Image(8, 40, 8, 8)),
        }
        self.set_draw_layer(Layer.hud)

    def draw(self):
        state = GameState.player_state
        p_pos = GameState.player.pos
        remain_hp = GameState.player.hp
        p_jump = state["max_jump"] - GameState.player.jump_cnt
        offset = Vector2D(3, 3) + p_pos
        px.rectb(*(self.pos + p_pos), WIDTH // 4 + 10, HEIGHT // 2, ORANGE)
        px.rectb(
            *(self.pos + p_pos + Vector2D(1, 1)),
            WIDTH // 4 - 2 + 10,
            HEIGHT // 2 - 2,
            YELLOW,
        )

        for i in range(state["hp"]):
            pos = self.pos + Vector2D(i * 8, 0) + offset
            self.sprites["damaged-hp"].draw(pos)
        for i in range(remain_hp):
            pos = self.pos + Vector2D(i * 8, 0) + offset
            self.sprites["hp"].draw(pos)
        for i in range(p_jump):
            pos = self.pos + Vector2D(i * 8, 8) + offset
            self.sprites["jump"].draw(pos)
        if state["slide"]:
            pos = self.pos + Vector2D(0, 16) + offset
            self.sprites["slide"].draw(pos)

        for i in range(state["keys"]):
            pos = self.pos + Vector2D(i * 8, 24) + offset
            self.sprites["key"].draw(pos)

        dmg_pos = self.pos + Vector2D(0, 32) + offset
        px.text(*dmg_pos, f"atk : {state['max_bullet']}", WHITE)


class MiniMapHUD(Drawable):
    def __init__(self):
        self.pos = Vector2D(-WIDTH // 4 + 10, HEIGHT // 4)
        self.set_draw_layer(Layer.hud)

    def draw(self):
        maps = GameState.map_state
        p_pos = GameState.player.pos
        offset = p_pos + Vector2D(3, 3)
        pos = self.pos + offset
        px.rectb(*(self.pos + p_pos), WIDTH // 4 * 3 - 10, HEIGHT // 2, ORANGE)
        px.rectb(
            *(self.pos + p_pos + Vector2D(1, 1)),
            WIDTH // 4 * 3 - 2 - 10,
            HEIGHT // 2 - 2,
            YELLOW,
        )

        for idx, map in enumerate(maps):
            if idx in GameState.visited_map:
                mx, my, mw, mh = tuple(p // 2 for p in map["xywh"])
                xywh = tuple(p * 8 for p in map["xywh"])
                if is_in(*p_pos, *xywh):
                    px.rect(*(pos + Vector2D(mx, my)), mw, mh, ORANGE)
                px.rectb(*(pos + Vector2D(mx, my)), mw, mh, WHITE)

                # NOTE: draw doors
                for linked_idx in map["link_to"]:
                    linked_xywh = tuple(p * 8 for p in maps[linked_idx]["xywh"])
                    if xywh[0] > linked_xywh[0]:
                        px.rect(*(pos + Vector2D(mx, my)), 1, mh, RED)
                    else:
                        px.rect(*(pos + Vector2D(mx + mw - 1, my)), 1, mh, RED)
