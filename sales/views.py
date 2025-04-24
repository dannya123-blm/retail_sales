from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render
from .models import Item, Order  # Assuming you have an Item model


def order_summary(request, order_id):
    # Fetch order by ID or return 404 if not found
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'sales/order_summary.html', {'order': order})

def complete_order(request, order_id):
    # Fetch order by ID or return 404 if not found
    order = get_object_or_404(Order, id=order_id)
    
    # Mark the order as completed
    order.status = Order.COMPLETED
    order.save()
    
    # Redirect to the order summary page
    return redirect('order_summary', order_id=order.id)
def create_order(request):
    if request.method == 'POST':
        # Handle the form submission to create a new order
        item_ids = request.POST.getlist('items')  # List of selected items (if any)
        items = Item.objects.filter(id__in=item_ids)
        
        # Create a new order
        order = Order.objects.create(
            user=request.user,  # Assuming you're using user authentication
        )
        
        # Add items to the order
        order.items.set(items)
        order.save()
        
        return redirect('order_success')  # Redirect to a success page (create one)

    # If the request method is GET, render the order creation form
    items = Item.objects.all()  # Get all items to choose from
    return render(request, 'sales/create_order.html', {'items': items})

def item_list(request):
    items = Item.objects.all()  # Retrieve all items from the database
    return render(request, 'sales/item_list.html', {'items': items})

def setup_users():
    # Hardcode users and assign roles (Admin, Sales Manager, Sales Associate, Customer)
    admin = User.objects.create_user(username='admin', password='adminpass')
    admin.save()
    
    sales_manager = User.objects.create_user(username='sales_manager', password='managerpass')
    sales_manager.save()

    sales_associate = User.objects.create_user(username='sales_associate', password='associatepass')
    sales_associate.save()

    customer = User.objects.create_user(username='customer', password='customerpass')
    customer.save()

    # You can assign roles using a custom role model or permissions
    admin.is_staff = True  # Admin can access the Django admin site
    admin.save()

    # Repeat for other roles as necessary
    # For instance, assign permissions or roles using Django's Group model or custom models
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/items/')  # Redirect after login
        else:
            error_message = 'Invalid username or password'
            return render(request, 'sales/login.html', {'error_message': error_message})

    return render(request, 'sales/login.html')
