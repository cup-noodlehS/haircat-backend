from django.contrib import admin
from .models.service import Service, ServiceImage, ServiceLabel, Label

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_services', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    readonly_fields = ('created_at',)

class ServiceLabelInline(admin.TabularInline):
    model = ServiceLabel
    extra = 1
    readonly_fields = ('created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialist', 'price', 'duration_minutes', 'points', 'average_rating')
    list_filter = ('specialist', 'created_at')
    search_fields = ('name', 'description', 'specialist__user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceImageInline, ServiceLabelInline]

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('service', 'image', 'order', 'created_at')
    list_filter = ('service',)
    readonly_fields = ('order', 'created_at')

@admin.register(ServiceLabel)
class ServiceLabelAdmin(admin.ModelAdmin):
    list_display = ('service', 'label', 'created_at')
    list_filter = ('service', 'label')
    search_fields = ('service__name', 'label__name')
    readonly_fields = ('created_at',)
