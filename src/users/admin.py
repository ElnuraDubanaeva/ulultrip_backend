from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_verified")
    list_display_links = ("username",)
    search_fields = ("email", "username")
    view_on_site = False
    fields = (
        "email",
        "username",
        "is_superuser",
        "is_verified",
        "is_active",
        "is_staff",
        "password",
        "favorite_tour",
    )

    readonly_fields = ("is_verified", "password")


admin.site.register(User, UserAdmin)
