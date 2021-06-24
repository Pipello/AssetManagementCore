from django.http import HttpResponse
from .models import Order, Bag
from .serializers import OrderSerializer, BagSerializer
from rest_framework import viewsets


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all().order_by("date")
    serializer_class = OrderSerializer


class BagViewSet(viewsets.ModelViewSet):

    queryset = Bag.objects.all()
    serializer_class = BagSerializer
