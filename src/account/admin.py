from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Customer,
    Specialist,
    RewardPoints,
    DayAvailability,
    DayOff,
    BarberShop,
    BarberShopImage,
    Barber,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "phone_number",
        "location",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "location")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "location",
                    "pfp",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                ),
            },
        ),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "total_points", "created_at", "updated_at")
    search_fields = ("user__first_name", "user__last_name", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ("user", "average_rating", "reviews_count", "point_to_php", "created_at", "updated_at")
    search_fields = ("user__first_name", "user__last_name", "user__email", "bio")
    readonly_fields = ("created_at", "updated_at")


@admin.register(RewardPoints)
class RewardPointsAdmin(admin.ModelAdmin):
    list_display = ("customer", "specialist", "points", "created_at")
    search_fields = (
        "customer__user__first_name",
        "customer__user__last_name",
        "specialist__user__first_name",
        "specialist__user__last_name",
    )
    readonly_fields = ("created_at",)
    list_filter = ("created_at", "specialist")


@admin.register(DayAvailability)
class DayAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("specialist", "day_of_week_display", "start_time", "end_time")
    list_filter = ("day_of_week", "specialist")
    search_fields = ("specialist__user__first_name", "specialist__user__last_name")


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ("specialist", "type_display", "date", "created_at")
    list_filter = ("type", "date", "specialist")
    search_fields = ("specialist__user__first_name", "specialist__user__last_name")
    readonly_fields = ("created_at",)


class BarberShopImageInline(admin.TabularInline):
    model = BarberShopImage
    extra = 1


class BarberInline(admin.TabularInline):
    model = Barber
    extra = 1


@admin.register(BarberShop)
class BarberShopAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [BarberShopImageInline, BarberInline]


@admin.register(BarberShopImage)
class BarberShopImageAdmin(admin.ModelAdmin):
    list_display = ("barber_shop", "image", "order", "created_at")
    list_filter = ("barber_shop",)
    search_fields = ("barber_shop__name", "image__name")
    ordering = ("barber_shop", "order")


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('name', 'barber_shop', 'average_rating', 'reviews_count', 'created_at')
    list_filter = ('barber_shop', 'created_at')
    search_fields = ('name', 'barber_shop__name')
    readonly_fields = ('created_at', 'updated_at')
