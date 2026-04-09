from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_item', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'user', 'cart', 'placed_at', 'total_price', 'items']
        read_only_fields = ['user', 'cart', 'placed_at', 'total_price', 'items']


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
