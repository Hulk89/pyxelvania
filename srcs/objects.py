from time import time

import pyxel as px
from srcs.constants import HEIGHT, YELLOW, BLUE
from srcs.vector import Vector2D
from srcs.base import (
    Sprite,
    ASprite,
    Image,
    Drawable,
    Updatable,
    Layer,
    CircleCollisionInterface,
)


class _Object(CircleCollisionInterface, Drawable):
    def __init__(self, pos, image):
        self.sprite = Sprite(image)
        super().__init__(pos, 8, 8)
        self.set_draw_layer(Layer.obj)

    def draw(self):
        self.sprite.draw(self.pos)

    def update_gamestate(self, state):
        pass

    def remove(self):
        self.stop_draw()


class _AObject(CircleCollisionInterface, Drawable, Updatable):
    def __init__(self, pos, images, freq):
        self.sprite = ASprite(images, freq)
        super().__init__(pos, 8, 8)
        self.set_draw_layer(Layer.obj)
        self.start_update()

    def update(self, dt, t):
        self.sprite.update(dt, t)

    def draw(self):
        self.sprite.draw(self.pos)

    def update_gamestate(self, state):
        pass

    def remove(self):
        self.stop_draw()
        self.stop_update()


class Text(Drawable, Updatable):
    def __init__(self, text):
        for t in reversed(Layer.popup_text):
            t.remove()

        self.time = time()
        self.text = text
        self.set_draw_layer(Layer.popup_text)
        self.start_update()

    def update(self, dt, t):
        if t - self.time > 2:
            self.stop_draw()
            self.stop_update()

    def draw(self):
        # TODO: 마음에 안들어...
        from srcs.state import GameState

        draw_pos = GameState.player.pos + Vector2D(-len(self.text) * 2, HEIGHT // 4)

        px.text(*(draw_pos + Vector2D(-1, 0)), self.text, BLUE)
        px.text(*(draw_pos + Vector2D(1, 0)), self.text, BLUE)
        px.text(*(draw_pos + Vector2D(0, -1)), self.text, BLUE)
        px.text(*(draw_pos + Vector2D(0, 1)), self.text, BLUE)
        px.text(*draw_pos, self.text, YELLOW)

    def remove(self):
        self.stop_draw()
        self.stop_update()


class KeyObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(16, 16, 8, 8))

    def update_gamestate(self, state):
        state["keys"] += 1


class SlideObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(0, 40, 8, 8))

    def update_gamestate(self, state):
        Text("You can slide!!")
        state["slide"] = True


class DJumpObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(8, 40, 8, 8))

    def update_gamestate(self, state):
        Text("one more jump!")
        state["max_jump"] += 1


class CKPTObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 32, 8, 8), Image(24, 32, 8, 8)], 0.4)

    def update_gamestate(self, state):
        Text("checkpoint saved")
        state["ckpt_pos"] = self.pos


class HeartObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 40, 8, 8), Image(24, 40, 8, 8)], 0.4)

    def update_gamestate(self, state):
        from srcs.state import GameState

        Text("one more heart")
        state["hp"] += 1
        GameState.player.hp = state["hp"]


class NPCObject1(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(48, 16, 8, 8), Image(56, 16, 8, 8)], 0.4)

    def update_gamestate(self, state):
        from srcs.state import GameState

        Text("Thank you!!")
        GameState.player.add_hp(1)


class NPCObject2(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(48, 24, 8, 8), Image(56, 24, 8, 8)], 0.4)

    def update_gamestate(self, state):
        from srcs.state import GameState

        Text("Thank you!!")
        GameState.player.add_hp(2)
