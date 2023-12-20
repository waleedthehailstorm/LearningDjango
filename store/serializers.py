from rest_framework.serializers import ModelSerializer
from .models import Customer, Order, OrderItem


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'order': {'required': False}}


class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item in order_items:
            OrderItem.objects.create(order=item, **item)
        return order

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items')
        instance.order_items.all().delete()
        for item in order_items:
            OrderItem.objects.create(order=instance, **item)
        return instance
