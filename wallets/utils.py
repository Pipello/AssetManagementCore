from pycoingecko import CoinGeckoAPI
from django.conf import settings


def update_prices():
    from .views import BagViewSet

    bags_query = BagViewSet.queryset
    cg = CoinGeckoAPI()
    prices = cg.get_price(
        ids=settings.GECKO_COINS,
        vs_currencies=settings.BASE_CURRENCY,
    )
    for bag in bags_query:
        price = prices[bag.asset][settings.BASE_CURRENCY]
        bags_query.filter(asset=bag.asset).update(actual_price=price)
