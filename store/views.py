from store.serializers import CustomerSerializer, OrderSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import mixins, status
from store.models import Customer, Order
from rest_framework import generics
from functools import wraps


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


def custom_response_format(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        try:
            if isinstance(response, Response):
                print("RESPONSE : ", response.data)
                print("RESPONSE STATUS CODE : ", response.status_code, response.status_text)
                if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                    return response
                if args[0].method == 'GET':
                    try:
                        if response.data.get('results'):
                            return response
                        if isinstance(response.data, dict) and 'pk' in kwargs:
                            response.data = {
                                'count': 0 if response.status_code == status.HTTP_404_NOT_FOUND else 1,
                                'next': None,
                                'previous': None,
                                'results': response.data,
                            }
                        if isinstance(response.data, list):
                            response.data = {
                                'count': len(response.data),
                                'next': None,
                                'previous': None,
                                'results': response.data,
                            }
                    except AttributeError:
                        response.data = {
                            'count': len(response.data),
                            'next': None,
                            'previous': None,
                            'results': response.data,
                        }
                if args[0].method == 'POST':
                    for key, value in response.data.items():
                        print(f"KEY AND VALUE IS {key} || {value}")
                    response.data = {
                        'message': "Record created successfully." if response.status_code == status.HTTP_201_CREATED else "Record not found.",
                        'results': response.data,
                    }
                if args[0].method in ['PUT', 'PATCH']:
                    response.data = {
                        'message': "Record updated successfully." if response.status_code == status.HTTP_200_OK else "Record not found.",
                        'results': response.data,
                    }
                if args[0].method == 'DELETE':
                    response.data = {
                        'message': "Record deleted successfully." if response.status_code == status.HTTP_204_NO_CONTENT else "Record not found.",
                        'results': {},
                    }
            return response
        except Exception as e:
            print("CUSTOM RESPONSE FORMAT EXC : ", e)
            response.data = {
                'message': "Something went wrong",
                'results': {},
            }
            return response
    return wrapper


@method_decorator(custom_response_format, name='dispatch')
class CustomerListModelMixinView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # BELOW LIST FUNCTION IS PROVIDED BY LIST MODEL MIXIN AND BELOW WE OVERRIDE THE DEFAULT FUNCTION TO ADD CUSTOM FUNCTIONALITY TO IT.
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     return Response(serializer.data)


@method_decorator(custom_response_format, name='dispatch')
class CustomerCreateModelMixin(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerUpdateModelMixin(mixins.UpdateModelMixin, generics.GenericAPIView):
    # queryset = Customer.objects.filter()
    serializer_class = CustomerSerializer

    # lookup_field = 'id'

    def get_queryset(self):
        queryset = Customer.objects.filter(first_name__icontains=self.request.query_params.get('first_name'))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


@method_decorator(custom_response_format, name="dispatch")
class CustomerDeleteModelMixin(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@method_decorator(custom_response_format, name='dispatch')
class CustomerAllModelMixins(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['email']
    search_fields = ['first_name']

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@method_decorator(custom_response_format, name='dispatch')
class OrderAllModelMixins(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin, mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'customer__first_name', 'customer__last_name']

    def handle_exception(self, exc):
        if isinstance(exc, Exception):
            message = {
                'message': "Something went wrong",
                'results': {},
            }
            print("ORDER EXC : ", exc)
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        request.data['customer'] = self.request.query_params.get('customer_id')

    def get_queryset(self):
        queryset = Order.objects.filter(customer_id=self.request.query_params.get('customer_id'))
        return queryset

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
