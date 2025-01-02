import math


class Vector2D:
    def __init__(self, x=0, y=0):
        self.values = (x, y)

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[1]

    @x.setter
    def x(self, value):
        self.values = (value, self.y)

    @y.setter
    def y(self, value):
        self.values = (self.x, value)

    def inner(self, other):
        return sum(a * b for a, b in zip(self, other))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.inner(other)
        elif isinstance(other, int) or isinstance(other, float):
            product = tuple(a * other for a in self)
            return Vector2D(*product)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            divided = tuple(a / other for a in self)
            return Vector2D(*divided)
        else:
            raise ValueError(f"Unsupported type: {type(other)}")

    def __add__(self, other):
        added = tuple(a + b for a, b in zip(self, other))
        return Vector2D(*added)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        subbed = tuple(a - b for a, b in zip(self, other))
        return Vector2D(*subbed)

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return str(self.values)

    def clamp(self, minvec, maxvec):
        clamped = tuple(
            max(min(v, maxv), minv) for v, minv, maxv in zip(self, minvec, maxvec)
        )
        return Vector2D(*clamped)

    def angle_between(self, other):
        v1 = self.normalize()
        v2 = other.normalize()
        return math.acos(v1.inner(v2))

    def dist_between(self, other):
        return (other - self).norm()

    def norm(self):
        return math.sqrt(sum(comp**2 for comp in self))

    def normalize(self):
        """Returns a normalized unit vector"""
        norm = self.norm()
        normed = tuple(comp / norm for comp in self)
        return Vector2D(*normed)

    def rotate(self, *args):
        if len(args) == 1 and isinstance(args[0], int) or isinstance(args[0], float):
            return self._rotate2D(*args)
        elif len(args) == 1:
            matrix = args[0]
            if not all(len(row) == len(v) for row in matrix) or not len(matrix) == len(
                self
            ):
                raise ValueError(
                    "Rotation matrix must be square and same dimensions as vector"
                )
            return self.matrix_mult(matrix)

    def _rotate2D(self, theta):
        theta = math.radians(theta)
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc * x - ds * y, ds * x + dc * y
        return Vector2D(x, y)

    def matrix_mult(self, matrix):
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError("Matrix must match vector dimensions")

        product = tuple(Vector2D(*row) * self for row in matrix)

        return Vector2D(*product)
