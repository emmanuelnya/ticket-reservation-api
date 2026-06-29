from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Pannello admin per il modello User personalizzato, con il campo role visibile."""

    fieldsets = UserAdmin.fieldsets + (("Ruolo", {"fields": ("role",)}),)
    list_display = ["username", "email", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff", "is_active"]
