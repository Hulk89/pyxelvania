from .base import (
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


class KeyObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(16, 16, 8, 8))

    def update_gamestate(self, state):
        state["keys"] += 1


class SlideObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(0, 40, 8, 8))

    def update_gamestate(self, state):
        state["slide"] = True


class DJumpObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(8, 40, 8, 8))

    def update_gamestate(self, state):
        state["max_jump"] += 1


class CKPTObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 32, 8, 8), Image(24, 32, 8, 8)], 0.4)

    def update_gamestate(self, state):
        state["ckpt_pos"] = self.pos


class HeartObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 40, 8, 8), Image(24, 40, 8, 8)], 0.4)

    def update_gamestate(self, state):
        state["hp"] += 1
