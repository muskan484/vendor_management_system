from loguru import logger
from django.db.models import Sum
from rest_framework import status
from django.utils import timezone
from rest_framework import generics ,views
from rest_framework.response import Response
from django.db.models.functions import Round
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (VendorSerializer,
                          PurchaseOrderSerialzer,
                          HistoricalPerfromanceSerializer)

class ListCreateVendor(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class RetrieveUpdateDeleteVendor(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class ListCreatePurchaseOrder(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerialzer

class RetrieveUpdateDeletePurchaseOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerialzer

    def perform_update(self, serializer):
        serializer.save()
        vendor = serializer.validated_data['vendor']
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status ='completed')

        # calculating on time delivery rate
        try:
            on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
            if completed_pos.count() == 0:
                on_time_delivery_rate =  0.0
            else:
                on_time_delivery_rate =  (on_time_deliveries/completed_pos.count()) * 100
        except Exception as e:
            logger.error(f'In calculating on time delivery rate -> {e}')

        # calculating quality rating avg
        try:
            avg_rating = completed_pos.exclude(quality_rating__isnull = True).aggregate(total_ratings = Sum("quality_rating"))['total_ratings']/completed_pos.count()
        except Exception as e:
            logger.error(f'In calculating quality rating average -> {e}')

        # calculating fullfilment rate
        try:
            total_pos = PurchaseOrder.objects.filter(vendor=vendor)
            successful_fulfillments = completed_pos.filter(issue_date__isnull=False, acknowledgment_date__isnull=False).count()
            if total_pos.count() == 0:
                fulfilment_rate =  0.0
            else:
                fulfilment_rate = Round((successful_fulfillments / total_pos.count()) * 100, 2)
        except ZeroDivisionError as e:
           logger.error(f'In calculating fullfilment rate -> {e}')


        # updating the Vendor model
        Vendor.objects.filter(name=vendor).update(
            on_time_delivery_rate = on_time_delivery_rate,
            quality_rating_avg = avg_rating,
            fulfilment_rate = fulfilment_rate
            )
        
        # updating HistoricalPerformance model
        HistoricalPerformance.objects.filter(vendor=vendor).update(
            on_time_delivery_rate = on_time_delivery_rate,
            quality_rating_avg = avg_rating,
            fulfilment_rate = fulfilment_rate
        )

class VendorPerformanceDetail(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerfromanceSerializer


class AcknowledgePurchaseOrder(views.APIView):
    def calculate_average_response_time(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
        if completed_pos.exists():
            total_response_time = timezone.timedelta(0)
            for po in completed_pos:
                total_response_time += po.acknowledgment_date - po.issue_date
            average_response_time = total_response_time / len(completed_pos)
            return Round(average_response_time.total_seconds() / 60.0, 2)
        else:
            return 0.0

    def get(self, request, *args, **kwargs):
        po_id = kwargs['pk']
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if purchase_order.acknowledgment_date:
            return Response({"error": "Purchase Order has already been acknowledged"}, status=status.HTTP_400_BAD_REQUEST)

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Trigger recalculation of average_response_time
        vendor = purchase_order.vendor
        average_response_time = self.calculate_average_response_time(vendor)
        vendor.average_response_time = average_response_time
        vendor.save()
        HistoricalPerformance.objects.filter(vendor=vendor).update(
            average_response_time = average_response_time,
        )

        return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)