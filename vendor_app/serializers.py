from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','name', 'contact_details', 'address', 'vendor_code']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg',
                  'average_response_time', 'fulfillment_rate']