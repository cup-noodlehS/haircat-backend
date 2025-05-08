from django.contrib import admin
from .models.service import Service, ServiceImage, ServiceLabel, Label
from .models.appointment import Appointment, Review, ReviewImage, AppointmentMessageThread, AppointmentMessage


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "total_services", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    readonly_fields = ("created_at",)


class ServiceLabelInline(admin.TabularInline):
    model = ServiceLabel
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "specialist",
        "price",
        "duration_minutes",
        "points",
        "average_rating",
    )
    list_filter = ("specialist", "created_at")
    search_fields = ("name", "description", "specialist__user__username")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ServiceImageInline, ServiceLabelInline]


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ("service", "image", "order", "created_at")
    list_filter = ("service",)
    readonly_fields = ("order", "created_at")


@admin.register(ServiceLabel)
class ServiceLabelAdmin(admin.ModelAdmin):
    list_display = ("service", "label", "created_at")
    list_filter = ("service", "label")
    search_fields = ("service__name", "label__name")
    readonly_fields = ("created_at",)


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    readonly_fields = ("order", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("appointment", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("appointment__customer__user__full_name", "comment")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ReviewImageInline]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review", "image", "order", "created_at")
    list_filter = ("review", "created_at")
    readonly_fields = ("order", "created_at")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("customer", "service", "schedule", "status", "created_at")
    list_filter = ("status", "schedule", "created_at")
    search_fields = ("customer__user__full_name", "service__name", "notes")
    readonly_fields = ("created_at", "updated_at")
