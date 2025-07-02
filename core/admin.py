from django.contrib import admin
from .models import Master, Order, Service, Review

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_active')
    filter_horizontal = ('services',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'master', 'appointment_date', 'status')
    list_filter = ('status', 'master', 'appointment_date') 
    filter_horizontal = ('services',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'is_published')