from rest_framework import serializers

from .models import Order, OrderItems

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'status']
        read_only_fields = ['id', 'status']
        extra_kwargs = {
            'user_id': {'required': True}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        # calculate total price
        total = sum(item['price'] * item['quantity'] for item in items_data)
        validated_data['total_price'] = total

        order = Order.objects.create(**validated_data)

        # create order items
        for item_data in items_data:
            OrderItems.objects.create(order=order, **item_data)
        return order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'product', 'quantity', 'price']
        read_only_fields = ['id']
        extra_kwargs = {
            'order': {'required': True},
            'product': {'required': True},
            'quantity': {'required': True},
            'price': {'required': True}
        }