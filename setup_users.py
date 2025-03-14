# setup_users.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_sales.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

users = [
    {"username": "admin", "email": "admin@amin.com", "password": "password", "group": "Admin", "is_superuser": True, "is_staff": True},
    {"username": "manager", "email": "manager@manager.com", "password": "password", "group": "Sales Manager", "is_staff": True},
    {"username": "associate", "email": "associate@associate.com", "password": "password", "group": "Sales Associate", "is_staff": True},
    {"username": "user1", "email": "user1@user1.com", "password": "password", "group": "Customer", "is_staff": False},
]

for u in users:
    user, created = User.objects.get_or_create(
        username=u["username"],
        defaults={
            "email": u["email"],
            "password": make_password(u["password"]),
            "is_superuser": u.get("is_superuser", False),
            "is_staff": u.get("is_staff", False)
        }
    )
    group = Group.objects.get(name=u["group"])
    user.groups.clear()
    user.groups.add(group)

print("Users created and assigned to roles successfully.")
