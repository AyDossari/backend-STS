from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetilView,
    DriverRequestDetailView,
    CustomerSignupView,
    DriverSignupView,
    CustomerDetilView,
    DriverDetilView, 
    DriverRequestListCreateView
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Test, api!"})

urlpatterns = [
    path('api/test/', test_api),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetilView.as_view(), name='product-detail'),
    path('driver-requests/', DriverRequestListCreateView.as_view(), name='driver-request-create'),
    path('driver-requests/<int:pk>/', DriverRequestDetailView.as_view(), name='driver-request-detail'),
    path('signup/customer/', CustomerSignupView.as_view(), name='signup-customer'),
    path('signup/driver/', DriverSignupView.as_view(), name='signup-driver'),
    path('customer/profile/', CustomerDetilView.as_view(), name='customer-profile'),
    path('driver/profile/', DriverDetilView.as_view(), name='driver-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]