from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product', 'product_name', 'quantity', 'price', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'address', 'placed_at', 'total_price')
	search_fields = ('user__username', 'id')
	list_filter = ('placed_at',)
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'product_name', 'quantity', 'price', 'total_price')
	search_fields = ('order__id', 'product_name')
