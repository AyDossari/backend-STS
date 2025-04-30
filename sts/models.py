from django.db import models

# Create your models here.


class Customer(models.Model):
    full_name = models.CharField(max_length=50)
    
    # From django docs `https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-options`
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    
    def __str__(self):
        return self.full_name
    
class Driver(models.Model):
    full_name = models.CharField(max_length=50)    
    email = models.EmailField(unique=True)
    vehicle_type = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    
    def __str__(self):
        return self.full_name
    
class Product(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products') 
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    
    # From django docs `https://docs.djangoproject.com/en/4.2/ref/models/fields/#default`
    status = models.CharField(max_length=20, default='Pending')   
    
    def __str__(self):
        return self.name