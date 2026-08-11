from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product ,Customer
from rest_framework.test import APIClient
# Create your tests here.

class ProductAccessTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.user_a = User.objects.create_user(username='ahmed', password='TestPass123!')
        self.customer_a = Customer.objects.create(user=self.user_a, full_name='Ahmed', address='Riyadh', phone_number='0555555555')
        
        self.user_b = User.objects.create_user(username='sara', password='TestPass123!')
        self.customer_b = Customer.objects.create(user=self.user_b, full_name='Sara', address='Jeddah', phone_number='0566666666' )
        
        self.product = Product.objects.create(customer = self.customer_a, name='Test Box', description='Test', weight=5.5)
    
    def test_products_access(self):
        self.client.force_authenticate(user=self.user_b)
        
        response = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 403)
        