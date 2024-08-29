class Vector2d:
    typecode = 'd'
    
    def __init__(self, x, y) -> None:
        self.__x = float(x) # Закритий атрибут
        self.__y = float(y)
    
    @property # помічує метод читання атрибута
    def x(self): # назва така ж як і атрибута
        return self.__x # просто повернути

    @property # так само і для інш атрибута
    def y(self):
        return self.__y
    
    def __iter__(self):
        return (i for i in (self.x, self.y)) # всі анші методи, які просто читають значення атрибутів залишаються без змін АЛЕ тепер це self.x виклик метод читання атрибута