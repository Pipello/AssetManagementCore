from rest_framework import serializers
from .models import Order, Bag


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "date",
            "amount",
            "price",
            "bag",
            "order_type",
            "earnings",
            "average_buy_price",
        ]
        read_only_fields = [
            "earnings",
            "wallet_value",
            "average_buy_price",
        ]


class BagSerializer(serializers.ModelSerializer):
    orders_list = serializers.SerializerMethodField()
    global_earning = serializers.SerializerMethodField()
    bag_tax = serializers.SerializerMethodField()

    class Meta:
        model = Bag
        fields = [
            "id",
            "asset",
            "global_earning",
            "actual_price",
            "average_buy_price",
            "amount",
            "symbol",
            "orders_list",
            "bag_tax",
        ]

    def get_orders_list(self, obj):
        out = []
        for order in obj.orders.all().order_by("date"):
            out.append(OrderSerializer(order).data)
        return out

    def get_global_earning(self, obj):
        orders = self.get_orders_list(obj)
        earnings = 0
        for order in orders:
            earnings += order["earnings"]
        return earnings

    def get_bag_tax(self, obj):
        if self.get_global_earning(obj) < 0:
            return 0
        return self.get_global_earning(obj) * 0.3
