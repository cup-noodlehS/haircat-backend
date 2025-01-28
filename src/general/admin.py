from django.contrib import admin
from .models import File, Location


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "x_coordinate", "y_coordinate")
    search_fields = ("name",)
