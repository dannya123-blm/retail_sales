from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    items = Item.objects.all()
    if request.method == 'POST':
        item_id = request.POST['item']
        quantity = int(request.POST['quantity'])
        item = get_object_or_404(Item, id=item_id)

        # Create or get current user's pending order
        order, created = Order.objects.get_or_create(customer=request.user, status='PENDING')

        # Check if item already in order
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item, defaults={'quantity': quantity, 'item_price': item.price})
        if not created:
            order_item.quantity += quantity
            order_item.save()

        return redirect('order_summary')

    return render(request, 'sales/order_create.html', {'items': items})
