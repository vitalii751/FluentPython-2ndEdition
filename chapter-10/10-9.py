Promotion = Callable[[Order], Decimal]

promos: list = []  # Глобальний на рівні модуля


def promotion(promo: Promotion) -> Promotion:  # Повертає функц без змін АЛЕ додає в регістр
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """Обчисл найб скидку"""
    return max(f_promo(order) for f_promo in promos)  # Ніяких змін не треба бо залежить від списка


@promotion  # Додаєм в регістр
def fidelite_promo(
    order: Order,
):  # Абстрактного класу більше немає і кожна функц є стратегією
    """5-% скидка для замовників, які мають не менше 1000балів лояльності"""

    if order.customer.fidelity >= 1000:
        return order.total() * Decimal("0.05")
    return Decimal(0)


@promotion
def bulk_item_promo(order: Order):
    """10% скидка для кожн позиції ЛайнІтем, де заказано не менше 20 одиниць"""

    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal("0.1")
        return discount


@promotion
def large_order_promo(order: Order):
    """7% скидка для заказів, вкл не менше 10 різних позицій"""

    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal("0.07")
    return Decimal(0)
