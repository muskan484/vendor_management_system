from django.urls import path
from .views import (
    ListCreateVendor, 
    RetrieveUpdateDeleteVendor, 
    ListCreatePurchaseOrder, 
    RetrieveUpdateDeletePurchaseOrder,
    VendorPerformanceDetail,
    AcknowledgePurchaseOrder)

urlpatterns = [
    path("vendors/", ListCreateVendor.as_view()),
    path("vendors/<int:pk>", RetrieveUpdateDeleteVendor.as_view()),
    path("vendors/<int:pk>/performance",VendorPerformanceDetail.as_view()),
    path('purchase_orders/', ListCreatePurchaseOrder.as_view()),
    path('purchase_orders/<int:pk>',RetrieveUpdateDeletePurchaseOrder.as_view()),
    path('purchase_orders/<int:pk>/acknowledge',AcknowledgePurchaseOrder.as_view())
]