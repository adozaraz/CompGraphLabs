class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)

        return Point(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)

        return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Point):
            raise NotImplemented("Figuring out")

        return Point(self.x * other, self.y * other)

    def __floordiv__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring out')

        return Point (self.x // other, self.y // other)

    def __truediv__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring out')

        return Point(self.x / other, self.y / other)

    def __mod__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring out')

        return Point(self.x % other, self.y % other)

    def __pow__(self, power, modulo=None):
        return Point(self.x ** power, self.y ** power)

    def __iadd__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __isub__(self, other):
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self

    def __imul__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring Out')
        self.x -= other
        self.y -= other
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring Out')
        self.x //= other
        self.y //= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring Out')
        self.x /= other
        self.y /= other
        return self

    def __imod__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring Out')
        self.x %= other
        self.y %= other
        return self

    def __ipow__(self, other):
        if isinstance(other, Point):
            raise NotImplemented('Figuring Out')
        self.x **= other
        self.y **= other
        return self
