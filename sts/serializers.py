from rest_framework import serializers
from .models import Customer, Driver, Product, DriverRequest

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class DriverSrializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DriverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRequest
        fields = '__all__'        