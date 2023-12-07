from rest_framework.serializers import ModelSerializer
from .models import Customer


class CustomerSerializer(ModelSerializer):

    # def create(self, validated_data):
    #     ...

    class Meta:
        model = Customer
        fields = '__all__'
