from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Order, Promotion, Collection
from django.db.models import Sum, Count, Max, Min, Avg
from rest_framework.generics import ListCreateAPIView



def say_hello(request):
    return HttpResponse('Bye World')


def nigga_world(request):
    raw_query = Order.objects.raw('SELECT * FROM store_order')
    result = Order.objects.filter().aggregate(order_count=Count('id'), product_sold_count=Count('orderitem__product_id'))
    return render(request, 'hello.html', {'name': 'SIGMA', 'result': result})


def debugging_code(request):
    x = 1
    y = 2
    z = x + y
    return HttpResponse(z)
