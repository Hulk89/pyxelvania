from time import time
import pyxel as px

from srcs.state import GameState
from srcs.constants import RED, GREEN
from srcs.base import (
    Updatable,
    Drawable,
    CircleCollisionInterface,
    ASprite,
    Image,
    Layer,
)
from srcs.vector import Vector2D
from srcs.utils import push_back, colliding_wall
from srcs.fireball import FireBall
from srcs.particles import ParticlesExplosion

PLAYER = {
    "idle": {"frames": [(8, 0, 8, 8), (24, 0, 8, 8)], "loop": True},
    "run": {"frames": [(8, 0, 8, 8), (16, 0, 8, 8)], "loop": True},
    "attack": {"frames": [(8, 8, 8, 8), (16, 8, 8, 8)], "loop": False},
    "jump-up": {"frames": [(24, 0, 8, 8), (24, 8, 8, 8)], "loop": True},
    "jump-down": {"frames": [(24, 0, 8, 8)], "loop": False},
    "slide": {"frames": [(24, 0, 8, 8), (32, 0, 8, 8)], "loop": False},
}
FREQ = 0.2


def on_pressed_left():
    return px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT) or px.btn(px.KEY_LEFT)


def on_pressed_right():
    return px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT) or px.btn(px.KEY_RIGHT)


def on_pressed_slide():
    return px.btnp(px.GAMEPAD1_BUTTON_B) or px.btnp(px.KEY_Z)


def on_pressed_jump():
    return px.btnp(px.GAMEPAD1_BUTTON_A) or px.btnp(px.KEY_SPACE)


def on_pressed_attack():
    return px.btnp(px.GAMEPAD1_BUTTON_X) or px.btnp(px.KEY_X)


class Player(CircleCollisionInterface, Updatable, Drawable):
    def __init__(self, pos, hp):
        self.jump_cnt = 0
        self.direction_right = True
        self.dx = 0
        self.dy = 0
        self.vel = 40
        self.hp = hp
        self.state = "idle"
        self.is_damaged = False
        self.damaged_time = time()
        self.asprites = {
            k: ASprite([Image(*uvwh) for uvwh in v["frames"]], FREQ, loop=v["loop"])
            for k, v in PLAYER.items()
        }
        super().__init__(pos, 8, 8)
        self.start_update()
        self.set_draw_layer(Layer.obj)

    @property
    def sprite(self):
        return self.asprites[self.state]

    @property
    def img(self):
        return self.sprite.img

    def change_state(self, state):
        if state != self.state:
            self.state = state
            self.asprites[state].reset()

    def add_hp(self, hp):
        self.hp = min(self.hp + hp, GameState.player_state["hp"])

    def damaged(self, direction_left, dmg):
        if not self.is_damaged:
            self.damaged_time = time()
            self.is_damaged = True
            self.hp = max(0, self.hp - dmg)
            dpos = Vector2D(-8 if direction_left else 8, -4)
            self.dy = 0
            x, y = push_back(*self.pos, *dpos)
            self.pos = Vector2D(x, int(y))

            ParticlesExplosion(
                self.pos + Vector2D(4, 4),
                [RED, RED, GREEN],
                duration=0.2,
                num_particles=10,
                vel_range=(5, 10),
            )

    def update(self, dt, t):
        # NOTE: position delta calculation
        self.dy += 0.5
        if on_pressed_left():
            self.direction_right = False
            self.dx = -self.vel * dt
        elif on_pressed_right():
            self.direction_right = True
            self.dx = self.vel * dt
        else:
            self.dx = 0

        if self.state == "slide":
            self.dx *= 1.3  # NOTE: faster move

        # NOTE: state assign
        if on_pressed_jump() and self.jump_cnt < GameState.player_state["max_jump"]:
            self.jump_cnt += 1
            self.state = "jump-up"
            self.change_state("jump-up")
            self.dy = -4
        elif on_pressed_slide() and GameState.player_state["slide"]:
            self.change_state("slide")
        elif on_pressed_attack():
            self.change_state("attack")
            fb_len = len([f for f in Layer.fg if isinstance(f, FireBall)])
            if fb_len < GameState.player_state["max_bullet"]:
                if self.direction_right:
                    fb_pos = self.pos + Vector2D(8, 3)
                else:
                    fb_pos = self.pos + Vector2D(0, 3)
                _ = FireBall(fb_pos, self.direction_right)
        elif self.state not in ["jump-up", "jump-down", "attack", "slide"]:
            if on_pressed_left() or on_pressed_right():
                self.change_state("run")
            else:
                self.change_state("idle")

        # NOTE: position update
        self.dy = min(4, max(-6, self.dy))
        x, y = push_back(*self.pos, self.dx, self.dy, self.state == "slide")
        self.pos = Vector2D(x, int(y))

        # NOTE: state transition
        if self.state == "jump-up" and self.dy > 0:
            self.change_state("jump-down")
        elif self.state == "jump-down" and colliding_wall(x, y + 1, self.dy > 0)[0]:
            self.change_state("idle")
        elif self.state == "attack" and self.sprite.is_ended:
            self.change_state("idle")
        elif self.state == "slide" and (t - self.sprite.start_t) > 0.5:
            self.change_state("idle")

        if colliding_wall(x, y + 1, self.dy > 0)[0]:
            self.jump_cnt = 0

        if (t - self.damaged_time) > 1:
            self.is_damaged = False
        # NOTE: sprite update frame
        self.sprite.update(dt, t)

    def draw(self):
        self.img.flip = not self.direction_right
        if self.is_damaged:
            px.dither(0.5)
        self.sprite.draw(self.pos)
        px.dither(1)
