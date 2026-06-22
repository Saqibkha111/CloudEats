from django.contrib import admin
from .models import Dish, Order, OrderItem
from .models import Dish

# @admin.register(Dish)
# class DishAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'is_available', 'created_at')
#     list_filter = ('is_available',)
#     search_fields = ('name', 'description')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')


admin.site.register(Order)
admin.site.register(OrderItem)
