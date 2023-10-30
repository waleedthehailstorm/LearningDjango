from django.urls import path
from . import views

# URL config
urlpatterns = [
    path('bye-world/', views.say_hello),
    path('hello-world/', views.nigga_world),
    path('debugging-code/', views.debugging_code),
]
