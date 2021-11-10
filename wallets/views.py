from django.http import HttpResponse
from .models import Order, Bag
from .serializers import OrderSerializer, BagSerializer
from .utils import update_prices
from rest_framework.response import Response
from rest_framework import viewsets


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all().order_by("date")
    serializer_class = OrderSerializer

    def create(self, *args, **kwargs):
        update_prices()
        data = self.request.data
        data["bag"] = Bag.objects.get(pk=data.get("bag"))
        if data.get("order_type", "") == "SELL":
            data["average_buy_price"] = data["bag"].average_buy_price
            bags = Bag.objects.all()
            data["wallet_value"] = 0
            for bag in bags:
                data["wallet_value"] += bag.amount * data["price"]

        Order.objects.create(
            amount=data.get("amount"),
            price=data.get("price"),
            bag=data.get("bag"),
            order_type=data.get("order_type"),
            average_buy_price=data.get("average_buy_price", 0),
            wallet_value=data.get("wallet_value", 0),
        )
        return HttpResponse(status=201)


class BagViewSet(viewsets.ModelViewSet):

    queryset = Bag.objects.all()
    serializer_class = BagSerializer


class TaxesViewSet(viewsets.ViewSet):
    queryset = Bag.objects.all()

    def list(self, request):
        total_tax = 0
        for bag in self.queryset:
            total_tax += BagSerializer(bag).data["global_earning"]
        if total_tax < 0:
            total_tax = 0
        return Response({"tax": total_tax * 0.3})
