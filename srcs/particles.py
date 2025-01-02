from random import uniform, randint, choice

import pyxel as px

from .constants import GREEN
from .base import Updatable, Drawable, Layer
from .vector import Vector2D


class Particle:
    sizes = {1: Vector2D(0, 0), 2: Vector2D(0, 1), 3: Vector2D(1, 1)}

    def __init__(self, pos, radius, vel, acc, duration, color):
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.remain_time = duration
        self.color = color

    @property
    def is_ended(self):
        return self.remain_time < 0

    def update(self, dt):
        self.remain_time -= dt
        self.vel += self.acc * dt
        self.pos += self.vel * dt

    def draw(self):
        dim = Particle.sizes[self.radius]
        px.rect(*self.pos, *dim, self.color)


class ParticlesExplosion(Updatable, Drawable):
    def __init__(
        self,
        pos,
        colors=[GREEN],
        duration=0.5,
        num_particles=30,
        vel_range=(10, 30),
        acceleration=-0.5,
    ):
        self.start_update()
        self.set_draw_layer(Layer.fg)

        self.particles = []
        for _ in range(num_particles):
            size = randint(1, 3)
            dist = randint(*vel_range)  # distance per seconds
            vel = Vector2D(dist, 0)
            vel = vel.rotate(uniform(0, 360))
            acc = vel.normalize() * acceleration  # deceleration
            self.particles.append(
                Particle(pos, size, vel, acc, duration, choice(colors))
            )

    def update(self, dt, t):
        if len(self.particles):
            for p in self.particles:
                p.update(dt)
                if p.is_ended:
                    self.particles.remove(p)
                    del p
        else:
            self.stop_draw()
            self.stop_update()

    def draw(self):
        for p in self.particles:
            p.draw()
