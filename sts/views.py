from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product , DriverRequest
from .serializers import ProductSerializer , DriverRequestSerializer

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
        serializer = ProductSerializer(product ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer._errors, status= 200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=204)    
    
    
class DriverRequestDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DriverRequest, pk=pk)

    def get(self, request, pk):
        driver_request = self.get_object(pk)
        serializer = DriverRequestSerializer(driver_request)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        driver_request = self.get_object(pk)
        serializer = DriverRequestSerializer(driver_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        driver_request = self.get_object(pk)
        driver_request.delete()
        return Response(status=204)    
    