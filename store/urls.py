from django.urls import path
from . import views

urlpatterns = [
    path('customer-list-model-mixin', views.CustomerListModelMixinView.as_view(), name='customer-list'),
    path('customer-create-model-mixin', views.CustomerCreateModelMixin.as_view(), name='create-customer'),
    path('customer-update-model-mixin/<int:pk>', views.CustomerUpdateModelMixin.as_view(), name='update-customer'),
    path('customer-delete-model-mixin/<int:pk>', views.CustomerDeleteModelMixin.as_view(), name='delete-customer'),
    path('customer-all-model-mixin', views.CustomerAllModelMixins.as_view(), name='list-and-post-customer'),
    path('customer-all-model-mixin/<int:pk>', views.CustomerAllModelMixins.as_view(), name='update-and-delete-customer'),
    path('order-all-model-mixin', views.OrderAllModelMixins.as_view(), name='list-and-post-order'),
    path('order-all-model-mixin/<int:pk>', views.OrderAllModelMixins.as_view(), name='update-and-delete-order'),
]
