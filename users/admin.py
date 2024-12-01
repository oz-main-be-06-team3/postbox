from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Users


class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ("email", "nickname", "phone", "is_active", "staff", "admin")
    list_filter = ("is_active", "staff")
    search_fields = ("email", "nickname", "phone")
    readonly_fields = ("staff",)
    ordering = ("email",)
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("nickname", "name", "phone")}),
        ("Permissions", {"fields": ("is_active", "staff", "admin")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nickname", "name", "password1", "password2", "is_active", "staff", "admin"),
            },
        ),
    )


admin.site.register(Users, CustomUserAdmin)
