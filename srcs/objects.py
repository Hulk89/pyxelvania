from .base import Sprite, ASprite, Image, Drawable, Updatable, Layer


class _Object(Drawable):
    def __init__(self, pos, image):
        self.pos = pos
        self.sprite = Sprite(image)
        self.set_draw_layer(Layer.obj)

    def draw(self):
        self.sprite.draw(self.pos)


class _AObject(Drawable, Updatable):
    def __init__(self, pos, images, freq):
        self.pos = pos
        self.sprite = ASprite(images, freq)
        self.set_draw_layer(Layer.obj)
        self.start_update()

    def update(self, dt, t):
        self.sprite.update(dt, t)

    def draw(self):
        self.sprite.draw(self.pos)


class KeyObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(16, 16, 8, 8))


class SlideObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(0, 40, 8, 8))


class DJumpObject(_Object):
    def __init__(self, pos):
        super().__init__(pos, Image(8, 40, 8, 8))


class HeartObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 32, 8, 8), Image(24, 32, 8, 8)], 0.4)


class CKPTObject(_AObject):
    def __init__(self, pos):
        super().__init__(pos, [Image(16, 40, 8, 8), Image(24, 40, 8, 8)], 0.4)
