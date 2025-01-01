from time import time
from abc import ABC, abstractmethod

import pyxel as px

from .constants import PURPLE

class Layer:
    bg = []  # 배경
    obj = []  # 캐릭터, object
    fg = []  # 화염구, effect


class Updatable(ABC):
    updatables = []

    @abstractmethod
    def update(self, dt, t):
        pass
    def start_update(self):
        self.updatables.append(self)
    def stop_update(self):
        self.updatables.remove(self)


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

    def set_draw_layer(self, layer: list):
        if hasattr(self, "layer") and self in self.layer:
            self.stop_draw()
        self.layer = layer
        self.start_draw()

    def start_draw(self):
        self.layer.append(self)

    def stop_draw(self):
        self.layer.remove(self)

class CircleCollisionInterface:
    def __init__(self, pos, w, h):
        self.pos = pos
        self.w = w
        self.h = h
        self.radius = (w + h) / 4

    def collide_with(self, entity):
        x, y = self.pos
        e_x, e_y =  entity.pos
        dist_square = (e_x - x) ** 2 + (e_y - y) ** 2
        rad_square = (self.radius + entity.radius) ** 2

        return rad_square >= dist_square



class Image:
    def __init__(self, u, v, w, h, flip=False,bank=0):
        self.bank = bank
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.flip = flip

    def __iter__(self):
        if self.flip:
            w = -self.w
        else:
            w = self.w
        return (self.bank, self.u, self.v, w, self.h).__iter__()


class Sprite:
    def __init__(self, img, colkey=PURPLE):
        self.img = img
        self.colkey = colkey

    def draw(self, pos):
        px.blt(*pos, *self.img, colkey=self.colkey)


class ASprite(Sprite):
    def __init__(self, frames, freq, colkey=PURPLE, loop=True):
        """
        frames : list[Image]
        frame_count : 이미지 순서
        freq: 바뀔 주기 (s)
        pt: prev_update time
        loop: loop를 돌지 말지
        img: Image (draw할 때 요걸 한다.)
        is_ended: 애니메이션이 끝났는지...
        """
        self.frames = frames
        self.frame_count = 0
        self.freq = freq
        self.pt = time()
        self.start_t = time()
        self.loop = loop
        self.img = frames[self.frame_count]
        self.is_ended = False
        super().__init__(self.img, colkey=colkey)

    def reset(self):
        self.frame_count = 0
        self.start_t = time()
        self.is_ended = False

    def update(self, _, t):
        """
        t: 현재 시간(times()) 
        """
        if t - self.pt >= self.freq:
            self.frame_count += 1
            self.pt = t
        if self.frame_count >= len(self.frames):
            if self.loop:
                self.frame_count = 0
            else:
                self.is_ended = True
        if not self.is_ended:
            self.img = self.frames[self.frame_count]
