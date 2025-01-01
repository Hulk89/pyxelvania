import pyxel as px

from .base import (
    Updatable,
    Drawable,
    CircleCollisionInterface,
    ASprite,
    Image,
)

from .utils import push_back, is_colliding

PLAYER = {
    "idle":      {"frames": [(8,0,8,8), (24,0,8,8)],  "loop": True,  "cboxes": None},
    "run":       {"frames": [(8,0,8,8), (16,0,8,8)],  "loop": True,  "cboxes": None},
    "attack":    {"frames": [(8,8,8,8), (16,8,8,8)],  "loop": False, "cboxes": None},
    "jump-up":   {"frames": [(24,0,8,8), (24,8,8,8)], "loop": True,  "cboxes": [(0,1,8,7), (0,0,8,8)]},
    "jump-down": {"frames": [(24,0,8,8)],             "loop": False, "cboxes": [(0,1,8,7)]},
    "slide":     {"frames": [(24,0,8,8), (32,0,8,8)], "loop": False, "cboxes": [(0,1,8,7), (0,2,8,6)]},
}
FREQ = 0.2


def on_pressed_left():
    return px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT) or \
           px.btn(px.KEY_LEFT)

def on_pressed_right():
    return px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT) or \
           px.btn(px.KEY_RIGHT)

def on_pressed_slide():
    return px.btnp(px.GAMEPAD1_BUTTON_B) or \
           px.btnp(px.KEY_Z)


def on_pressed_jump():
    return px.btnp(px.GAMEPAD1_BUTTON_A) or \
           px.btnp(px.KEY_SPACE)

def on_pressed_attack():
    return px.btnp(px.GAMEPAD1_BUTTON_X) or \
           px.btnp(px.KEY_X)


class Player(CircleCollisionInterface, Updatable, Drawable):
    def __init__(self, pos):
        self.direction_right = True
        self.dx = 0
        self.dy = 0

        self.state = "idle"
        self.asprites = {k: ASprite([Image(*uvwh) for uvwh in v["frames"]],
                                    FREQ,
                                    loop=v["loop"])
                            for k, v in PLAYER.items()}
        super().__init__(pos, 8, 8)
        self.start_update()

    @property
    def sprite(self):
        return self.asprites[self.state]

    @property
    def img(self):
        return self.sprite.img

    def circle_collide_with(self, entity) -> bool:
        w, h = self.img.w, self.img.h
        x, y = self.pos
        e_w, e_h = entity.img.w, entity.img.h
        e_x, e_y =  entity.pos
        dist_square = (e_x - x) ** 2 + (e_y - y) ** 2

        rad = (w + h) / 4
        e_rad = (e_w + e_h) / 4
        rad_square = (rad + e_rad) ** 2


        return rad_square >= dist_square


    def update(self, dt, t):
        # NOTE: position delta calculation
        self.dy += 0.5
        if on_pressed_left():
            self.direction_right = False
            self.dx = -2
        elif on_pressed_right():
            self.direction_right = True
            self.dx = +2
        else:
            self.dx = 0

        # NOTE: state assign
        if on_pressed_jump():
            self.state = "jump-up"
            self.dy = -6
        elif on_pressed_slide():
            self.state = "slide"
            self.dx *= 1.5  # NOTE: faster move
        elif on_pressed_attack():
            self.state = "attack"
        elif self.state not in ["jump-up", "jump-down", "attack", "slide"]:
            if on_pressed_left() or on_pressed_right():
                self.state = "run"
            else:
                self.state = "idle"

        self.dy = min(6, max(-6, self.dy))
        # TODO: Bug!!
        #x, y = push_back(self.pos[0], self.pos[1], self.dx, self.dy)
        x, y = self.pos[0] + self.dx, self.pos[1] + self.dy

        print(x, y)
        self.pos = (x, self.pos[1])


        # NOTE: state transition
        if self.state == "jump-up" and self.dy >=0:
            self.state = "jump-down"
        if self.state == "jump-down" and is_colliding(x, y+1, True):
            self.state = "idle"

        self.sprite.update(dt, t)

    def draw(self):
        self.img.flip = (self.direction_right == False)
        print(self.img.flip)
        self.sprite.draw(self.pos)
