from django.db import models

# Create your models here.
class sale(models.Model):
    ProdName = models.CharField(max_length=255)
    ProdID = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    CustName = models.CharField(max_length=255,null=True)
    CustID = models.IntegerField(null=True)
    saleDate = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    class Meta:
        db_table = 'sale'

class Customer(models.Model):
    CustName = models.CharField(max_length=255)
    birthday = models.DateField(auto_now_add=False)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    class Meta:
        db_table='customer'