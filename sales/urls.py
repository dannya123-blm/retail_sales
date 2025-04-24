from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.item_list, name='items'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/summary/', views.order_summary, name='order_summary'),
    path('order/complete/<int:order_id>/', views.complete_order, name='complete_order'),
    path('accounts/login/', views.login_view, name='login'),
]
