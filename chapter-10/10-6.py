from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Callable, NamedTuple


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:  # Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[["Order"], Decimal]] = None  # звичайно анотація функц

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(
                self
            )  # тут просто для обрахунку скидки викликаємо функц
        return self.total() - discount

    def __repr__(self) -> str:
        return f"<Order total: {self.total():.2f} due: {self.due():.2f}>"


def fidelite_promo(
    order: Order,
):  # Абстрактного класу більше немає і кожна функц є стратегією
    """5-% скидка для замовників, які мають не менше 1000балів лояльності"""

    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


def bulk_item_promo(order: Order):
    """10% скидка для кожн позиції ЛайнІтем, де заказано не менше 20 одиниць"""

    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.1")
        return discount


def large_order_promo(order: Order):
    """7% скидка для заказів, вкл не менше 10 різних позицій"""

    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal("0.07")
    return Decimal(0)


promos = [fidelite_promo, bulk_item_promo, large_order_promo]

def best_promo(order: Order) -> Decimal:
    """Обчисл найб скидку"""
    return max(f_promo(order) for f_promo in promos)