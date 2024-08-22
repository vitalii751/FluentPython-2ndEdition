# Список promos будується шляхом просмотра глобального списку імен модуля
from decimal import Decimal
from strategy import Order
from strategy import (
	fidelity_promo, bulk_item_promo, large_order_promo # імпорт функц скидок, щоб були доступні в глобальному простору імен
)

promos = [promo for name, promo in globals().items() # перебір всіх імен
		 if name.endswith('_promo') and  # Залишити імена тільки з суфіксом _promo
		 name != 'best_promo' # Відфільтрувати саму функц шоб не було безкінечної рекурсії
		 ]

def best_promo(order: Order) -> Decimal: # функц без змін
	"""Обчисл найб скидку"""
    return max(f_promo(order) for f_promo in promos)