from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model to accommodate Role relationship
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Role {self.role_id}"

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')

    def __str__(self):
        return self.username

class RolePermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role, related_name='permissions')

    def __str__(self):
        return self.permission

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order #{self.order_id}"

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
