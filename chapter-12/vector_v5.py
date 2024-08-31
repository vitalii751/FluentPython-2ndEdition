from array import array
import reprlib
import math
import operator
import functools
import itertools # для метода __format__

class Vector:
    typecode = "d"
    __match_args__ = (
        "x",
        "y",
        "z",
        "t",
    )  # шоб була можливість співставлень з динамічнимм атр, вводити цей атр безвредно і + він вбиває двох зайців: - підтримк позиційних образцов в гілках case + збер імена динамічн атр, які підтрим __getattr__ __setattr__

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

    def __getattr__(self, name):
        cls = type(self)  # отр клас Vector
        try:
            pos = cls.__match_args__.index(name)  # спроба отр позицію
        except ValueError:  # якшо виключення, то ...
            pos = -1
        if 0 <= pos < len(self._components):  # якшо в межах повертаємо елем
            return self._components[pos]
        msg = f"{cls.__name__!r} object has no attribute {name!r}"  # якшо за межами то помилка
        raise AttributeError(msg)

    def __setattr__(self, name, value) -> None:
        cls = type(self)
        error = ""
        if len(name) == 1:  # спец обробка односимв атр
            if (
                name in cls.__match_args__
            ):  # коли атр є в списку в співствл, то одне повідомл
                error = "readonly attribute {attr_name!r}"
            elif name.islower():  # якшо строчна буква
                error = "cant set attribute 'a' to 'z' in {cls.__name__!r}"
            else:
                error = ""  # в ін випадках поле пусте
        if error:  # якшо поле не пусте
            msg = error.format(cls_name=cls.__name__, attr_name=name)
            raise AttributeError(msg)
        super().__setattr__(
            name, value
        )  # випадок по дефолту: виклик метод __setattr__ суперкласа для отримання стандартної поведінки

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components)  # ств генератор, бо економе память
        return functools.reduce(operator.xor, hashes, 0)  # 0 - ініціалізатор

    def angle(self, n): # обчисл одну з кутових коорд по формулі
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n - 1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 * a
        else:
            return a
        
    def angles(self): # ств генератор для обчисл всіх кутових коорд по запросу
        return (self.angle(n) for n in range(1, len(self)))
    
    def __format__(self, format_spec: str) -> str:
        if format_spec.endswith('h'): # гіперсферичні коорд
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles()) # chain - перебирає модуль і кутові вектора, ств генераторний вираз
            outer_format = '<{}>' # представлення в кутових скобках
        else:
            coords = self
            outer_format = '({})' # представл в круглих скобках 
        components = (format(c, format_spec) for c in coords) # відформатування коорд по запиту
        return outer_format.format(', '.join(components)) # представити все через кому, в кутових або круглих скобках