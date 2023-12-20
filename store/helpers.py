from .models import Order, OrderItem


def create_order_item(order, order_items):
    for order_item in order_items:
        OrderItem.objects.create(
            order=order.data.get('id'),
            product_id=order_item.get('product'),
            quantity=order_item.get('quantity'),
            unit_price=order_item.get('unit_price'),
        )
        