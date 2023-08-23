from django.db import models

# Create your models here.
class Product(models.Model):
    ProdName = models.CharField(max_length=255)
    BrandID = models.IntegerField()
    CategoryID = models.IntegerField()
    SupplierID = models.IntegerField()
    cost = models.IntegerField()
    price = models.IntegerField()
    class Meta:
        db_table = 'product'
class Category(models.Model):
    CategoryName = models.CharField(max_length=255)
    class Meta:
        db_table='category'
class Brand(models.Model):
    BrandName = models.CharField(max_length=255)
    class Meta:
        db_table='brand'
class Supplier(models.Model):
    SupplierName = models.CharField(max_length=255)
    class Meta:
        db_table='supplier'