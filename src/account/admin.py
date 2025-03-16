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
    AppointmentTimeSlot,
    QnaQuestion,
    QnaAnswer,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "phone_number",
        "is_staff",
        "is_specialist",
        "is_barber_shop",
        "is_customer",
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


class DayAvailabilityInline(admin.TabularInline):
    model = DayAvailability
    extra = 1


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "average_rating",
        "reviews_count",
        "barber_shop",

    )
    search_fields = ("user__first_name", "user__last_name", "user__email", "bio")
    readonly_fields = ("created_at", "updated_at")
    inlines = [DayAvailabilityInline]


class AppointmentTimeSlotInline(admin.TabularInline):
    model = AppointmentTimeSlot
    extra = 1

@admin.register(DayAvailability)
class DayAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("specialist", "day_of_week_display", "start_time", "end_time")
    list_filter = ("day_of_week", "specialist")
    search_fields = ("specialist__user__first_name", "specialist__user__last_name")
    inlines = [AppointmentTimeSlotInline]


@admin.register(AppointmentTimeSlot)
class AppointmentTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day_availability', 'start_time', 'end_time')
    list_filter = ('day_availability__day_of_week',)
    search_fields = ('day_availability__specialist__user__full_name',)



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
    list_display = (
        "name",
        "barber_shop",
        "average_rating",
        "reviews_count",
        "created_at",
    )
    list_filter = ("barber_shop", "created_at")
    search_fields = ("name", "barber_shop__name")
    readonly_fields = ("created_at", "updated_at")



@admin.register(QnaQuestion)
class QnaQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialist', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)


@admin.register(QnaAnswer) 
class QnaAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'question__specialist', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question__message', 'question__specialist')
    readonly_fields = ('created_at',)
