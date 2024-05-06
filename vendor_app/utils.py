from django.utils import timezone
from . models import Vendor, PurchaseOrder
from django.db.models import Count, Avg


def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    print("com",completed_pos)
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
    print("com--",on_time_deliveries)


    if completed_pos.count() > 0:
        on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100
        print("com--",on_time_delivery_rate)

    else:
        on_time_delivery_rate = 0.0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    print(vendor.on_time_delivery_rate)
    vendor.save()

def update_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)

    if acknowledged_pos.exists():
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in acknowledged_pos
            if po.acknowledgment_date is not None
        ]

        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
        else:
            avg_response_time = 0.0
    else:
        avg_response_time = 0.0

    vendor.average_response_time = avg_response_time
    vendor.save()