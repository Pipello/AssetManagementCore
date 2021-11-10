from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings


ORDER_TYPE = (
    ("BUY", "Buy"),
    ("SELL", "Sell"),
)


class Bag(models.Model):
    asset = models.CharField(_("asset"), default="bitcoin", max_length=254)
    actual_price = models.FloatField(_("actual price"), default=0)
    symbol = models.CharField(_("symbol"), default="BTC", max_length=5)

    def __str__(self):
        return self.asset

    @property
    def amount(self):
        orders = Order.objects.filter(bag__id=self.id)
        total = 0
        for order in orders:
            if order.order_type == "BUY":
                total += order.amount
            elif order.order_type == "SELL":
                total -= order.amount
        return total

    @property
    def average_buy_price(self):
        orders = Order.objects.filter(bag__id=self.id).order_by("date")
        average = 0
        bag_amount = 0
        for order in orders:
            if order.order_type == "BUY":
                average = average * bag_amount + order.amount * order.price
                bag_amount += order.amount
                average = average / bag_amount
            elif order.order_type == "SELL":
                bag_amount -= order.amount
        return average


class Order(models.Model):
    date = models.DateTimeField(_("order date"), default=timezone.now)
    amount = models.FloatField(_("amount"), default=0)
    price = models.FloatField(_("price"), default=0)
    bag = models.ForeignKey(
        Bag, related_name="orders", on_delete=models.CASCADE, null=False
    )
    order_type = models.CharField(
        _("order type"), choices=ORDER_TYPE, default="BUY", max_length=10
    )

    average_buy_price = models.FloatField(_("average buy price"), default=0)
    wallet_value = models.FloatField(_("wallet value"), default=0)

    def __str__(self):
        return str(self.amount)

    @property
    def earnings(self):
        if self.order_type == "BUY":
            return 0
        elif self.order_type == "SELL":
            return self.amount * (self.price - self.average_buy_price)
