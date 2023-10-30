from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    return HttpResponse('Bye World')


def nigga_world(request):
    return render(request, 'hello.html', {'name': 'Waleed'})


def debugging_code(request):
    x = 1
    y = 2
    z = x + y
    return HttpResponse(z)
