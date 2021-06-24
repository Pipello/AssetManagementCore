from django.contrib import admin
from .models import Bag, Order

# Register your models here.


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ["asset", "amount", "average_price"]


@admin.register(Order)
class OrderBag(admin.ModelAdmin):
    list_display = ["bag", "amount", "price", "order_type", "earnings", "sell_price"]
    list_filter = ["bag__asset"]
