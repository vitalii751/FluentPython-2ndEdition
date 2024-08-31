from array import array
import reprlib
import math
import operator


class Vector:
    typecode = "d"

    def __init__(self, components) -> None:
        self._components = array(
            self.typecode, components
        )  # ств "захищ" атр, який є array

    def __iter__(self):
        return iter(
            self._components
        )  # повертаємо просто ітератор з ітерабильного обьекта

    def __repr__(self) -> str:
        components = reprlib.repr(
            self._components
        )  # отримуємо представлення з лімітною довж. Напр: array('d',[1.0, 2.0, 3.0, ...])
        components = components[
            components.find("[") : -1
        ]  # Видал префікс array('d',[ і також видал остан скобку ')'
        return f"Vector({components})"

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(
            self._components
        )  # в байти переводимо масив з числами

    def __eq__(self, other) -> bool:
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(
            *self
        )  # Раніше до Python3.8 юзали: math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)  # передаємо зразу обьект memoryview

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):  # якшо аргумент типу slice
            cls = type(self)  # отримуєм клас екземп(тобто Vector)
            return cls(
                self._components[key]
            )  # отр новий екземпл класу, зарахунок зрізу масива _components
        index = operator.index(key)  # якшо можливо отр index по key
        return self._components[
            index
        ]  # то просто повертаємо один конкретний елем з _components
