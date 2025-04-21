from django.contrib import admin
from .models import User, Role, RolePermission, Category, Item, Order, OrderItem

admin.site.register(User)
admin.site.register(Role)
admin.site.register(RolePermission)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
