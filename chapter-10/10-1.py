from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


class Order(NamedTuple):  # Контекст
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional["Promotional"] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self) -> str:
        return f"<Order total: {self.total():.2f} due: {self.due()}:.2f>"


class Promotion(ABC):  # Стратегія абстрактний базовий клас
    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        """Повернути скидку у вигляді додатної суми в доларах"""


class FidelitePromo(Promotion):  # Перша конкретна стратегія
    """5-% скидка для замовників, які мають не менше 1000балів лояльності"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal("0.05")
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromo(Promotion):  # друга конкретна стратегія
    """10% скидка для кожн позиції ЛайнІтем, де заказано не менше 20 одиниць"""

    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal("0.1")
        return discount


class LargeOrderPromo(Promotion):  # третя конкретна стратегія
    """7% скидка для заказів, вкл не менше 10 різних позицій"""

    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal("0.07")
        return Decimal(0)
