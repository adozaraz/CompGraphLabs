class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    @z.setter
    def z(self, z):
        self.__z = z

