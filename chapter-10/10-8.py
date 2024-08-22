from decimal import Decimal
from inspect

from strategy import Order
import promotions # Тут повинні бути тільки функції-стратегії

promos = [func for _, func in inspect.getmembers(promotions, inspect.isfunctions)]

def best_promo(order: Order) -> Decimal:
    """Обчисл найб скидку"""
    return max(f_promo(order) for f_promo in promos)