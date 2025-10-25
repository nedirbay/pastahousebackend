from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'name', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'email', 'phone', 'address', 'note', 'total', 'status', 'items', 'created_at')
        read_only_fields = ('user', 'total', 'status', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        total = 0
        for item in items_data:
            product = item.get('product')
            qty = item.get('quantity', 1)
            OrderItem.objects.create(
                order=order,
                product=product,
                name=product.name,
                price=product.price,
                quantity=qty
            )
            total += product.price * qty
            if product.quantity >= qty:
                product.quantity -= qty
                product.in_stock = product.quantity > 0
                product.save()
        order.total = total
        order.save()
        return order
