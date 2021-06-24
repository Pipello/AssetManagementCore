from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

ASSETS = (
    ("BTC", "BTC"),
    ("ETH", "ETH"),
    ("LTC", "LTC"),
    ("AAVE", "AAVE"),
    ("XTZ", "XTZ"),
    ("GRT", "GRT"),
)

ORDER_TYPE = (
    ("BUY", "Buy"),
    ("SELL", "Sell"),
)


class Bag(models.Model):
    asset = models.CharField(_("asset"), choices=ASSETS, default="BTC", max_length=254)
    # TODO: Get that through API (market price)
    actual_price = models.FloatField(_("actual price"), default=0)

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
    def average_price(self):
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

    sell_price = models.FloatField(_("sell price"), default=0)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order_type == "SELL":
            self.sell_price = self.bag.average_price
        else:
            self.sell_price = 0
        super().save(*args, **kwargs)

    @property
    def earnings(self):
        if self.order_type == "BUY":
            return 0
        elif self.order_type == "SELL":
            return self.amount * (self.price - self.sell_price)
