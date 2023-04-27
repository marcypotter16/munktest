import math


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x, self.y = x, y
        self.length = math.sqrt(self.x ** 2 + self.y ** 2)
        self.sqr_length = self.x ** 2 + self.y ** 2

    def __mul__(self, other):
        """
        Pointwise multiplication
        :param other: another vector
        :return: the pointwise product
        """
        return Vector2(self.x * other.x, self.y * other.y)

    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __len__(self):
        return 2

    def __le__(self, other):
        return self.length <= other.length

    def __lt__(self, other):
        return self.length < other.length

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __str__(self):
        return f"({self.x}, {self.y})"
