from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="items", null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="orders", null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='PENDING')

    def update_total_amount(self):
        total = sum(item.quantity * item.item_price for item in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username if self.customer else 'Unknown'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, related_name="order_items", null=True)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Automatically set the item_price from the current Item price if not set
        if not self.item_price:
            self.item_price = self.item.price
        super().save(*args, **kwargs)
        # Update order total after saving each OrderItem
        self.order.update_total_amount()

    def __str__(self):
        return f"{self.quantity} x {self.item.name if self.item else 'Deleted Item'}"
