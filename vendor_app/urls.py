from django.urls import path
from .views import *
urlpatterns = [
    path('home', home),
    path('api/vendors/', VendorAPI.as_view()),
    path('api/vendors/<int:pk>/', VendorAPI.as_view()),
    path('api/purchase-orders/', PurchaseAPI.as_view()),
    path('api/purchase-orders/<int:pk>/', PurchaseAPI.as_view()),
    path('api/purchase_details/<int:pk>/', PurchaseAPI.as_view()),
    path('api/vendors/<int:vendor_id>/performance/', PerformanceAPI.as_view()),
     path('api/<str:id>/acknowledge/',
        OrderAcknowledge.as_view()),
]