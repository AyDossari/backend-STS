from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product , DriverRequest , Customer , Driver
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .serializers import ProductSerializer , DriverRequestSerializer , CustomerSerializer , DriverSrializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class ProductListCreateView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status= 200)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= 201)
        return Response(serializer.errors, status= 400)
    
    
class ProductDetilView(APIView):
    def get_object(self , pk):
        return get_object_or_404(Product, pk=pk )
    
    def get(self,request,pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)
    
    def patch(self,request,pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=204)    
    
    
class DriverRequestListCreateView(APIView):
    def get(self, request):
        requests = DriverRequest.objects.all()
        serializer = DriverRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DriverRequestSerializer(data=request.data)

        if serializer.is_valid():
            product_id = request.data.get('product')

            try:
                product = Product.objects.get(id=product_id)
             # From stack overflow `https://stackoverflow.com/questions/52575523/how-to-capture-the-model-doesnotexist-exception-in-django-rest-framework?utm_source=chatgpt.com`                
            except Product.DoesNotExist:
                return Response({"error": "Product not found."}, status=404)

            if product.status != "Pending":
                return Response({"error": "Product is already taken."}, status=400)
            driver_request = serializer.save()
            product.status = "Approved"
            product.save()

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
class DriverRequestDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DriverRequest, pk=pk)

    def get(self, request, pk):
        driver_request = self.get_object(pk)
        serializer = DriverRequestSerializer(driver_request)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        driver_request = self.get_object(pk)
        serializer = DriverRequestSerializer(driver_request, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # From DRF docs: `https://www.django-rest-framework.org/api-guide/serializers/#overriding-save-instances`
            new_status = serializer.validated_data.get('status')
            if new_status:
                product = driver_request.product

                if new_status == 'Accepted':
                    product.status = 'Approved'
                elif new_status == 'PickedUp':
                    product.status = 'PickedUp'
                elif new_status == 'Stored':
                    product.status = 'Stored'

                product.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        driver_request = self.get_object(pk)
        driver_request.delete()
        return Response(status=204)
    
class CustomerSignupView(APIView):
    
    def post(self, request):
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')

        try:
            validate_password(password)
        except ValidationError as err:
            return Response({'error': err.messages}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, full_name=full_name, address=address, phone_number=phone_number)   
        
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            },
            status=201
        ) 
        
class DriverSignupView(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        vehicle_type = request.data.get('vehicle_type')
        phone_number = request.data.get('phone_number')

        try:
            validate_password(password)
        except ValidationError as err:
            return Response({'error': err.messages}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        Driver.objects.create(user=user, full_name=full_name, vehicle_type=vehicle_type, phone_number=phone_number)
        
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            },
            status=201
        )
        
        
class CustomerDetilView(APIView):      
    def get(self , request):
        customer = Customer.objects.get(user = request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status= 200)
    
class DriverDetilView(APIView):
    def get(self , request):
        driver = Driver.objects.get(user = request.user)
        serializer = DriverSrializer(driver)
        return Response(serializer.data, status=200)        