from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg
from django.db.models import F
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,
                                                help_text='Average response time in hours')
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    PURCHASE_STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    QUALITY_RATING_CHOICES = [
        (1.0, "Poor"),
        (2.0, "Below Average"),
        (3.0, "Average"),
        (4.0, "Good"),
        (5.0, "Excellent"),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(
        max_length=50, choices=PURCHASE_STATUS, default='Pending')
    quality_rating = models.FloatField(
        choices=QUALITY_RATING_CHOICES, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    response_time = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,
                                        help_text='Time taken to acknowledge POs in hours')

    # def clean(self):
    #     if self.delivery_date <= self.order_date:
    #         raise ValidationError("Delivery date must be after order date.")

    def __str__(self):
        return f"{self.po_number}--{self.vendor}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.vendor.name

