from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Order, Bag


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "date",
            "amount",
            "price",
            "bag",
            "order_type",
            "sell_price",
            "earnings",
        ]


class BagSerializer(serializers.ModelSerializer):
    orders_list = serializers.SerializerMethodField()

    class Meta:
        model = Bag
        fields = ["asset", "actual_price", "average_price", "amount", "orders_list"]

    def get_orders_list(self, obj):
        out = []
        for order in obj.orders.all():
            out.append(
                {
                    "date": order.date,
                    "amount": order.amount,
                    "price": order.price,
                    "order_type": order.order_type,
                    "sell_price": order.sell_price,
                    "earnings": order.earnings,
                }
            )
        return out
