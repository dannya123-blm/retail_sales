from django.contrib import admin
from .models import Category, Item, Order, OrderItem

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
