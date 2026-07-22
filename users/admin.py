from django.contrib import admin

from .models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
    )
    list_filter = ("id",)
    search_fields = ("email",)
