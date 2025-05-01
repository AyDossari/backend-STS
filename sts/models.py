from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    full_name = models.CharField(max_length=50)
    # From django docs `https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#extending-the-existing-user-model`
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    
    def __str__(self):
        return self.full_name
    
class Driver(models.Model):
    full_name = models.CharField(max_length=50)    
    
    # From django docs `https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#extending-the-existing-user-model`
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    vehicle_type = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    
    def __str__(self):
        return self.full_name
    
class Product(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='products') 
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    
    # From django docs `https://docs.djangoproject.com/en/4.2/ref/models/fields/#default`
    status = models.CharField(max_length=20, default='Pending')  
    
    # From stack overflow `https://stackoverflow.com/questions/48438569/returning-hex-uuid-as-default-value-for-django-model-charfield`
    def generate_serial():
        return uuid.uuid4().hex[:8].upper() 
        
    serial_number = models.CharField(max_length=8,unique=True, default=generate_serial,editable=False)

    def __str__(self):
        return self.name
    
class DriverRequest(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, related_name='requests')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='driver_requests')
        
    # From django docs `https://docs.djangoproject.com/en/4.2/ref/models/fields/#default`
    status = models.CharField(max_length=20, default='Pending')
        
    # From django docs `https://docs.djangoproject.com/en/5.1/ref/models/fields/#datetimefield``
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f'{self.driver.full_name} , {self.product.name}'
       