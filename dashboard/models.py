from django.db import models

# Create your models here.
class purchase(models.Model):
    ProdName = models.CharField(max_length=255)
    ProdID = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    SupplierID = models.IntegerField()
    purchaseDate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255)
    total = models.IntegerField()
    class Meta:
        db_table = 'purchase'

class stock(models.Model):
    ProdName = models.CharField(max_length=255)
    ProdID = models.CharField(max_length=255)
    quantity = models.IntegerField()
    class Meta:
        db_table = 'stock'

class predict(models.Model):
    ProdID = models.IntegerField()
    weekDay = models.CharField(max_length=255)
    quantity = models.IntegerField()
    class Meta:
        db_table = 'predict'

class weekPredict(models.Model):
    ProdID = models.IntegerField()
    quantity = models.IntegerField()
    class Meta:
        db_table = 'weekPredict'