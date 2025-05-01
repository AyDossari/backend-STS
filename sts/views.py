from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

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
    
    