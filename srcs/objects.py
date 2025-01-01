
from .base import Sprite, Image, Drawable, Updatable, Layer
                    

class KeySprite(Drawable):
    def __init__(self, pos):
        self.pos = pos
        self.img = Sprite(Image(16, 16, 8, 8))
        self.set_draw_layer(Layer.obj)

    def draw(self):
        self.img.draw(self.pos)
