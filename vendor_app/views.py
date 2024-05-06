from django.shortcuts import render
from rest_framework.response import Response
from django.utils import timezone
from vendor_app.serializers import VendorSerializer, PurchaseSerializer,PerformanceSerializer
from rest_framework.views import APIView
from rest_framework import status
from vendor_app.models import Vendor, PurchaseOrder
from vendor_app.utils import *
from datetime import datetime, timezone

# Create your views here.
def responsedata(status, message, data=None):
    if status:
        return {"status":status,"message":message,"data":data}
    else:
        return {"status":status,"message":message,"data":data}
def home(request):
    pass
class VendorAPI(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Vendor created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        if pk:
            vendor=Vendor.objects.get(pk=pk)
            ven_ser=VendorSerializer(vendor)
            return Response(ven_ser.data)
        else:
            vendor=Vendor.objects.all()
            vendor_ser=VendorSerializer(vendor,many=True)
            return Response(vendor_ser.data)

    def put(self, request,pk=None):
        if pk:
            vendor=Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(vendor,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Vendor updated successfully","data":serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            vendor=Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response({"message":"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

class PurchaseAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            vendor_name = data.get('vendor_name')
            if not vendor_name:
                return Response(responsedata(False, "Vendor name is required"), status=status.HTTP_404_NOT_FOUND)

            serializer = PurchaseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Purchase created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(responsedata(False, "Something went wrong", str(err)), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,pk):
        print(pk)
        vendor=Vendor.objects.get(id=pk)
        purchase=PurchaseOrder.objects.filter(vendor=vendor)
        #print(purchase.count())

        serializer=PurchaseSerializer(purchase,many=True)
        return Response(serializer.data)
    def put(self, request,pk=None):
        purchase_order=PurchaseOrder.objects.get(pk=pk)
        serializer = PurchaseSerializer(purchase_order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Purchase updated successfully","data":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk=None):
        if pk is not None:
            purchase_order=PurchaseOrder.objects.get(pk=pk)
            purchase_order.delete()
            return Response({"message":"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

    def purchase_details(self, request,pk):
        if pk:
            print(pk)
            purchase=PurchaseOrder.objects.get(pk=pk)
            serializer=PurchaseSerializer(purchase,many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"Please provide the purchase id "},status=status.HTTP_404_NOT_FOUND)

class PerformanceAPI(APIView):
    def get(self, request, vendor_id):
        vendor=Vendor.objects.get(id=vendor_id)
        serializer=PerformanceSerializer(vendor)
        return Response(serializer.data)
#class Acknowleges

class OrderAcknowledge(APIView):
    def post(self, request, id=None):
        try:
            purchaseorder = PurchaseOrder.objects.get(po_number=id)
            print("GGGGG",purchaseorder)
            if purchaseorder.acknowledgment_date:
                print("ddd")
                return Response(responsedata(False, "Purchase order already acknowledged"),
                                status=status.HTTP_208_ALREADY_REPORTED)
            else:
                purchaseorder.acknowledgment_date = datetime.now()
                print(  "ddddd",purchaseorder.acknowledgment_date)
                purchaseorder.save()
                return Response(responsedata(True, "Purchase order acknowledged"),
                                status=status.HTTP_200_OK)

        except Exception as err:
            return Response(responsedata(False, "Something went wrong", str(err)),
                                status=status.HTTP_400_BAD_REQUEST)