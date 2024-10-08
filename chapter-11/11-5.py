from array import array
import math


class Vector2d:
    typecode = "d"  # атрибут класу, коли тре екземпляра пететв в байти і навпаки

    def __init__(self, x, y) -> None:
        self.x = float(x)  # корисно зразу перетв у тип float
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))  # завдяки цьому працює розпаковка
        # реаліз проста у вигляді генератора

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(
            class_name, *self
        )  # !r - правильне отримання їхнього представлення

    def __str__(self):
        return str(tuple(self))  # з ітер обьекта легко побудувати кортеж

    def __bytes__(self):
        return bytes(
            [ord(self.typecode)]
        ) + bytes(  # для генерації обьекта ми перетв typecode в bytes і конкатенируем
            array(self.typecode, self)
        )  # з обьектом bytes, отриман переобразованием масива, який побудований обходом екземпляра

    def __eq__(self, other) -> bool:
        return tuple(self) == tuple(
            other
        )  # для швидк порівняння. Це працює коли операнди є екземплярами класу, АЛЕ не без проблем

    def __abs__(self):
        return math.hypot(self.x, self.y)  # модуль вектора

    def __bool__(self):
        return bool(abs(self))  # перевірка довжини на bool

    @classmethod
    def frombytes(cls, octets):  # self - відсутнє, бо передаєм сам клас(cls)
        typecode = chr(octets[0])  # читаємо typecode з 1ого байту
        memv = memoryview(octets[1:]).cast(
            typecode
        )  # ств обьект memoryview з двійк послідовності і переводимо його в тип typecode
        return cls(*memv)  # Розпаковуєм і ств обьект, який необх конструктуру

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
