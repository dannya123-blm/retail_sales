# setup_roles.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_sales.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sales.mQodels import Category, Item, Order, OrderItem

# Define roles clearly
roles = {
    "Admin": {
        "models": [Category, Item, Order, OrderItem],
        "permissions": ['add', 'change', 'delete', 'view']
    },
    "Sales Manager": {
        "models": [Category, Item, Order, OrderItem],
        "permissions": ['add', 'change', 'delete', 'view']
    },
    "Sales Associate": {
        "models": [Order, OrderItem, Item],
        "permissions": ['add', 'change', 'view']  # Limited perms, no delete
    },
    "Customer": {
        "models": [Order, OrderItem, Item],
        "permissions": ['add', 'view']  # Customers only create/view orders
    }
}

# Dynamically create groups and assign permissions
for role_name, role_data in roles.items():
    group, created = Group.objects.get_or_create(name=role_name)
    group.permissions.clear()

    for model in role_data["models"]:
        content_type = ContentType.objects.get_for_model(model)
        for perm_name in role_data["permissions"]:
            codename = f"{perm_name}_{model._meta.model_name}"
            permission = Permission.objects.get(content_type=content_type, codename=codename)
            group.permissions.add(permission)

print("Roles and permissions set up successfully.")
