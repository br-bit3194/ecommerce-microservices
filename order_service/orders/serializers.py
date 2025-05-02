from rest_framework import serializers

from .models import Order, OrderItems


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'order': {'required': True},
            'product': {'required': True},
            'quantity': {'required': True},
            'price': {'required': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'status', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'total_price', 'created_at', 'updated_at']