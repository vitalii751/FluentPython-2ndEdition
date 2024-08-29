"""
Клас двухвимірного вектора

    >>> v1 = Vector2d(3, 4) 
    >>> print(v1.x, v1.y) 
    3.0 4.0
    >>> x, y = v1
    >>> x, y
    (3.0, 4.0)
    >>> v1
    Vector2d(3.0, 4.0)
    >>> v1_clone = eval(repr(v1)) 
    >>> v1_clone == v1
    True
    >>> print(v1) 
    (3.0, 4.0)
    >>> octets = bytes(v1)
    b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
    >>> abs(v1) 
    5.0
    >>> bool(v1), bool(Vector2d(0, 0)) 
    (True, False)
    
Тест методу класу ``.frombytes()``:

    >>> v1_clone = Vector2d.frombytes(bytes(v1)) 
    >>> v1_clone
    Vector2d(3.0, 4.0)
    >>> v1 == v1_clone
    True
    
Тест ``format()`` з декартовими коорд

    >>> format(v1) 
    '(3.0, 4.0)'
    >>> format(v1, '.2f') 
    '(3.00, 4.00)'
    >>> format(v1, '.3e') 
    '(3.000e+00, 4.000e+00)'
    >>> format(v1, '.3fp') 
    '<5.000 0.644'
    
Тест методу ``angle``::

    >>> Vector2d(0, 0).angle()
    0.0
    >>> Vector2d(1, 0).angle() 
    1.5707963267948966
    >>> epsilon = 10**-8
    >>> abs(Vector2d(0, 1).angle() - math.pi/2) < epsilon
    False
    >>> abs(Vector2d(1, 1).angle() - math.pi/4) < epsilon 
    True
    
Тест свойств, які доступні ТІКИ для читання:

    >>> v1.x, v1.y
    (3.0, 4.0)
    >>> v1.x = 999
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: property 'x' of 'Vector2d' object has no setter
    
Тести хешування:

    >>> v1 = Vector2d(3, 4) 
    >>> v2 = Vector2d(3.1, 4.2) 
    >>> len({v1, v2}) 
    2

"""

from array import array
import math


class Vector2d:
    __match_args__ = ("x", "y")

    typecode = "d"

    def __init__(self, x, y) -> None:
        self.__x = float(x)  #
        self.__y = float(y)

    @property  #
    def x(self):  #
        return self.__x  #

    @property  #
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))  #

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, other: object) -> bool:
        return tuple(self) == tuple(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.x, self.y)

    def __format__(self, fmt_spec: str = "") -> str:
        if fmt_spec.endswith("p"):  # формат закінч на букву 'p'
            fmt_spec = fmt_spec[:-1]  # видалити p
            coords = (abs(self), self.angle())  # кортеж для полярних коорд
            outer_fmt = "<{} {}"
        else:
            coords = self
            outer_fmt = "({}, {})"
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):  # self - відсутнє, бо передаєм сам клас(cls)
        typecode = chr(octets[0])  # читаємо typecode з 1ого байту
        memv = memoryview(octets[1:]).cast(
            typecode
        )  # ств обьект memoryview з двійк послідовності і переводимо його в тип typecode
        return cls(*memv)  # Розпаковуєм і ств обьект, який необх конструктуру
