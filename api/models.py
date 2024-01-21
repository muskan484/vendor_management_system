from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfilment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
       
class PurchaseOrder(models.Model):
    status_choice = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('canceled','Canceled'),
    ]
    po_number = models.CharField(max_length=50,unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name = 'vendors')  #foreign key will be the id key of vendor model that is created by drf
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20,choices=status_choice)
    quality_rating = models.FloatField(validators = [MinValueValidator(1),MaxValueValidator(5)],null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):  
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfilment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.vendor.name
    
    
    

