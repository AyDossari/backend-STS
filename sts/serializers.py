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
    customer = CustomerSerializer(read_only=True)    
    class Meta:
        model = Product
        fields = '__all__'
        # From stack overflow `https://stackoverflow.com/questions/41366832/django-rest-api-make-field-read-only-for-certain-permission-level`
        read_only_fields = ['customer']


class DriverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRequest
        fields = '__all__'  
        read_only_fields = ['driver']      